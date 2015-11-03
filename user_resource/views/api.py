import logging
from smtplib import SMTPException

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from oauth2_provider.ext.rest_framework.permissions import TokenHasScope
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from ..models import SentMessage
from ..oauth import DEFAULT_FIELDS, SCOPE_TO_FIELD_MAP, USER_FIELDS
from ..serializers import SendMailSerializer, UserSerializer

logger = logging.getLogger(__name__)


class UserViewset(viewsets.GenericViewSet):
    required_scopes = ['basic']
    permission_classes = [TokenHasScope]
    serializer_class = UserSerializer

    def get_queryset(self):
        token = self.request.auth
        user = token.user
        return User.objects.all().filter(pk=user.id)

    def list(self, request):
        user_queryset = self.get_queryset().first()
        fields = request.query_params.get('fields')
        granted_scopes = request.auth.scope
        granted_scopes = granted_scopes.split()
        granted_fields = []
        for scope in granted_scopes:
            granted_fields.extend(SCOPE_TO_FIELD_MAP[scope])

        if fields is None:
            fields = []
        else:
            fields = fields.split(',')
            fields = [field.strip() for field in fields if field.strip()]
        fields = set(fields)
        all_fields = set(DEFAULT_FIELDS + USER_FIELDS)
        undefined_fields = list(fields - all_fields)
        if undefined_fields:
            error_message = {
                'detail': 'fields (%s) not found' % ', '.join(undefined_fields)
            }
            return Response(error_message, status=HTTP_400_BAD_REQUEST)

        allowed_fields = list(set(fields).intersection(set(granted_fields)))
        user_serialized = UserSerializer(user_queryset, context={'fields': allowed_fields}).data
        return Response(user_serialized)

    @list_route(methods=['POST'], required_scopes=['send_mail'])
    def send_mail(self, request):
        token = request.auth
        app = token.application
        app_admin = token.application.user
        user = self.get_queryset().first()
        mail = SendMailSerializer(data=request.data)
        if mail.is_valid():
            subject = '[SSO] [%s] %s' % (app.name, mail.validated_data.get('subject'))
            body = ('%s\n\n\n'
                    'Sent via SSO by %s\n\n'
                    'You received this message because you\'ve provided the email sending'
                    ' permission to the application')
            body = body % (mail.validated_data.get('message'), app.name)
            from_email = '%s <%s>' % (app_admin.first_name, app_admin.email)
            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=[user.email],
                reply_to=mail.validated_data.get('reply_to'),
            )
            message = email_message.message()
            sent_message = SentMessage(
                message_id=message['Message-ID'],
                sender=app,
                user=user,
            )
            response_data = {
                'Message-ID': message['Message-ID'],
                'status': True,
            }
            try:
                email_message.send()
                sent_message.status = True
                response_data['status'] = True
            except SMTPException as err:
                sent_message.status = False,
                sent_message.error_message = err.message
                logger.error(err)
                response_data['status'] = False
            sent_message.save()
            return Response(response_data)
        else:
            return Response(mail.errors, status=HTTP_400_BAD_REQUEST)
