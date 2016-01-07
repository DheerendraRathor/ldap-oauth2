from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView
from oauth2_provider.exceptions import OAuthToolkitError
from oauth2_provider.http import HttpResponseUriRedirect
from oauth2_provider.models import get_application_model as get_oauth2_application_model
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views import AuthorizationView
from oauth2_provider.views.application import ApplicationRegistration

from core.utils import get_default_scopes

from .forms import RegistrationForm


class ApplicationRegistrationView(ApplicationRegistration):
    form_class = RegistrationForm


class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    """
    View used to update an application owned by the request.user
    """
    form_class = RegistrationForm
    context_object_name = 'application'
    template_name = "oauth2_provider/application_form.html"

    def get_queryset(self):
        return get_oauth2_application_model().objects.filter(user=self.request.user)


class CustomAuthorizationView(AuthorizationView):

    def form_valid(self, form):
        client_id = form.cleaned_data.get('client_id', '')
        application = get_oauth2_application_model().objects.get(client_id=client_id)
        scopes = form.cleaned_data.get('scope', '')
        scopes = set(scopes.split(' '))
        scopes.update(set(get_default_scopes(application)))
        private_scopes = application.private_scopes
        if private_scopes:
            private_scopes = set(private_scopes.split(' '))
            scopes.update(private_scopes)
        scopes = ' '.join(list(scopes))
        form.cleaned_data['scope'] = scopes
        return super(CustomAuthorizationView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        """
        Copied blatantly from super method. Had to change few stuff, but didn't find better way
        than copying and editing the whole stuff.
        Sin Count += 1
        """
        try:
            scopes, credentials = self.validate_authorization_request(request)
            try:
                del credentials['request']
                # Removing oauthlib.Request from credentials. This is not required in future
            except KeyError:  # pylint: disable=pointless-except
                pass

            kwargs['scopes_descriptions'] = [oauth2_settings.SCOPES[scope] for scope in scopes]
            kwargs['scopes'] = scopes
            # at this point we know an Application instance with such client_id exists in the database
            application = get_oauth2_application_model().objects.get(
                client_id=credentials['client_id'])  # TODO: cache it!
            kwargs['application'] = application
            kwargs.update(credentials)
            self.oauth2_data = kwargs
            # following two loc are here only because of https://code.djangoproject.com/ticket/17795
            form = self.get_form(self.get_form_class())
            kwargs['form'] = form

            # Check to see if the user has already granted access and return
            # a successful response depending on 'approval_prompt' url parameter
            require_approval = request.GET.get('approval_prompt', oauth2_settings.REQUEST_APPROVAL_PROMPT)

            # If skip_authorization field is True, skip the authorization screen even
            # if this is the first use of the application and there was no previous authorization.
            # This is useful for in-house applications-> assume an in-house applications
            # are already approved.
            if application.skip_authorization:
                uri, headers, body, status = self.create_authorization_response(
                    request=self.request, scopes=" ".join(scopes),
                    credentials=credentials, allow=True)
                return HttpResponseUriRedirect(uri)

            elif require_approval == 'auto':
                tokens = request.user.accesstoken_set.filter(application=kwargs['application']).all().order_by('-id')
                if len(tokens) > 0:
                    token = tokens[0]
                    if len(tokens) > 1:
                        # Enforce one token pair per user policy. Remove all older tokens
                        request.user.accesstoken_set.exclude(pk=token.id).all().delete()

                    # check past authorizations regarded the same scopes as the current one
                    if token.allow_scopes(scopes):
                        uri, headers, body, status = self.create_authorization_response(
                            request=self.request, scopes=" ".join(scopes),
                            credentials=credentials, allow=True)
                        return HttpResponseUriRedirect(uri)

            return self.render_to_response(self.get_context_data(**kwargs))

        except OAuthToolkitError as error:
            return self.error_response(error)
