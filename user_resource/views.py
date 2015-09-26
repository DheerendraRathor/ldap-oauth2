from collections import defaultdict

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

from .serializers import UserSerializer
from .oauth import scope_to_field_map, default_fields, user_fields
from .forms import InstituteAddressForm, ProgramForm


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

        allowed_fields = list(set(fields).intersection(set(granted_fields)))
        user_serialized = UserSerializer(user_queryset, context={'fields': allowed_fields}).data
        return Response(user_serialized)


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
            insti_address_form = InstituteAddressForm(initial=model_to_dict(user.instituteaddress))
        except AttributeError:
            insti_address_form = InstituteAddressForm()
        try:
            program_form = ProgramForm(initial=model_to_dict(user.program))
        except AttributeError:
            program_form = ProgramForm()
        return render(request, 'user_resources/home.html',
                      {
                          'insti_address_form': insti_address_form,
                          'program_form': program_form,
                      }
                      )
