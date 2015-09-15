from rest_framework import viewsets
from rest_framework.response import Response
from oauth2_provider.ext.rest_framework.permissions import TokenHasScope
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .oauth import scope_to_field_map, default_fields, user_fields
from rest_framework.status import HTTP_400_BAD_REQUEST


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
            fields = map(unicode.strip, fields)
        fields = set(fields)
        all_fields = set(default_fields + user_fields)
        undefined_fields = list(fields - all_fields)
        if undefined_fields:
            error_message = {
                'detail': 'fields (%s) not found' % ', '.join(undefined_fields)
            }
            return Response(error_message, status=HTTP_400_BAD_REQUEST)

        allowed_fields = set(fields).intersection(set(granted_fields))
        user_serialized = self.get_serializer(user_queryset, context={'fields': allowed_fields}).data
        return Response(user_serialized)
