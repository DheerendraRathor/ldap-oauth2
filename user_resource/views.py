from collections import defaultdict
from smtplib import SMTPException
import logging

from rest_framework import viewsets
from rest_framework.response import Response
from oauth2_provider.ext.rest_framework.permissions import TokenHasScope
from django.contrib.auth.models import User
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.views.generic import ListView, View
from braces.views import LoginRequiredMixin
from oauth2_provider.models import AccessToken
from oauth2_provider.settings import oauth2_settings
from django.shortcuts import redirect, render
from django.forms.models import model_to_dict
from rest_framework.decorators import list_route
from django.core.mail import EmailMessage

from .serializers import UserSerializer, SendMailSerializer
from .oauth import scope_to_field_map, default_fields, user_fields
from .forms import InstituteAddressForm, ProgramForm
from .models import Program, InstituteAddress, ContactNumber, SecondaryEmail, SentMessage

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
            granted_fields.extend(scope_to_field_map[scope])

        if fields is None:
            fields = []
        else:
            fields = fields.split(',')
            fields = [field.strip() for field in fields if field.strip()]
        fields = set(fields)
        all_fields = set(default_fields + user_fields)
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
            body = ('%s\n\n'
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
            response_data = {}
            try:
                email_message.send()
                sent_message.status = True
                response_data['status'] = True
            except SMTPException as e:
                sent_message.status = False,
                sent_message.error_message = e.message
                logger.error(e)
                response_data['status'] = False
            sent_message.save()
            return Response(response_data)
        else:
            return Response(mail.errors, status=HTTP_400_BAD_REQUEST)


class UserApplicationListView(LoginRequiredMixin, ListView):
    template_name = 'user_resources/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        user = self.request.user
        access_tokens = AccessToken.objects.filter(user=user).prefetch_related('application')

        application_scope_dict = defaultdict(set)

        for access_token in access_tokens:
            scopes = access_token.scope
            scopes = scopes.split()
            application_scope_dict[access_token.application] |= set(scopes)

        application_scope_detail_dict = {}
        for application, scopes in application_scope_dict.items():
            application_scope_detail_dict[application] = [oauth2_settings.SCOPES.get(scope, None) for scope in scopes if
                                                          oauth2_settings.SCOPES.get(scope, None)]

        return application_scope_detail_dict


class ApplicationRevokeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        AccessToken.objects.filter(user=user, application_id=pk).delete()
        return redirect('user:settings')


class UserHomePageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            insti_address_form = InstituteAddressForm(initial=model_to_dict(user.insti_address))
        except (AttributeError, InstituteAddress.DoesNotExist):
            insti_address_form = InstituteAddressForm()

        try:
            program_form = ProgramForm(initial=model_to_dict(user.program))
        except (AttributeError, Program.DoesNotExist):
            program_form = ProgramForm()

        mobile_numbers = ContactNumber.objects.all().filter(user=user).order_by('-id')
        secondary_emails = SecondaryEmail.objects.all().filter(user=user).order_by('-id')
        user_profile = user.userprofile
        gpo_email = user.email
        ldap_number = user_profile.mobile
        roll_number = user_profile.roll_number

        return render(request, 'user_resources/home.html',
                      {
                          'insti_address_form': insti_address_form,
                          'program_form': program_form,
                          'mobile_numbers': mobile_numbers,
                          'secondary_emails': secondary_emails,
                          'gpo_email': gpo_email,
                          'ldap_number': ldap_number,
                          'roll_number': roll_number,
                      }
                      )


class UpdateInstiAddressView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        try:
            insti_address = user.insti_address
        except InstituteAddress.DoesNotExist:
            insti_address = None
        form = InstituteAddressForm(data=request.POST, instance=insti_address)
        if form.is_valid():
            insti_address = form.save(commit=False)
            insti_address.user = user
            insti_address.save()
        return redirect('user:home')


class UpdateProgramView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        try:
            program = user.program
        except Program.DoesNotExist:
            program = None
        form = ProgramForm(data=request.POST, instance=program)
        if form.is_valid():
            program = form.save(commit=False)
            program.user = user
            program.save()
        return redirect('user:home')


class UpdateMobileNumberView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        mobiles = request.POST.getlist('phone')
        mobiles = set([mobile for mobile in mobiles if mobile != ''])
        saved_mobiles = set([contact.number for contact in user.contacts.all()])
        mobiles_to_update = mobiles - saved_mobiles
        mobiles_to_delete = saved_mobiles - mobiles
        if mobiles_to_update:
            ContactNumber.objects.bulk_create([ContactNumber(user=user, number=number) for number in mobiles_to_update])
        if mobiles_to_delete:
            ContactNumber.objects.filter(user=user).filter(number__in=mobiles_to_delete).delete()
        return redirect('user:home')


class UpdateSecondaryEmailView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        emails = request.POST.getlist('email')
        emails = set([email for email in emails if email != ''])
        saved_emails = set([secondary_email.email for secondary_email in user.secondary_emails.all()])
        emails_to_update = emails - saved_emails
        emails_to_delete = saved_emails - emails
        if emails_to_update:
            SecondaryEmail.objects.bulk_create([SecondaryEmail(user=user, email=email) for email in emails_to_update])
        if emails_to_delete:
            SecondaryEmail.objects.filter(user=user).filter(email__in=emails_to_delete).delete()
        return redirect('user:home')
