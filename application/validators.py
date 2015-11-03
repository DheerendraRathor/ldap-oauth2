from datetime import timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from oauth2_provider.models import get_application_model as get_oauth2_application_model
from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.settings import oauth2_settings

from core.utils import get_default_scopes


class CustomOAuth2Validator(OAuth2Validator):

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        application = get_object_or_404(get_oauth2_application_model(), client_id=client_id)
        return get_default_scopes(application)

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        request.scopes = list(set(request.scopes).union(set(get_default_scopes(client))))
        return super(CustomOAuth2Validator, self).validate_scopes(client_id, scopes, client, request, *args, **kwargs)

    def save_bearer_token(self, token, request, *args, **kwargs):
        """
        It's messy. It is 90% code from parent function. I didn't find a way to reduce it.
        I tried and I failed :'(
        Sin Count += 1


        Save access and refresh token, If refresh token is issued, remove old refresh tokens as
        in rfc:`6`
        """
        if request.refresh_token:
            # remove used refresh token
            # Copied as is from parent. I don't know why they're even caring to delete this! - Dheerendra
            try:
                RefreshToken.objects.get(token=request.refresh_token).revoke()
            except RefreshToken.DoesNotExist:
                assert ()  # TODO though being here would be very strange, at least log the error

        expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        token['expires_in'] = oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS

        if request.response_type == 'token':
            expires = timezone.now() + timedelta(seconds=settings.IMPLICIT_ACCESS_TOKEN_EXPIRES_SECONDS)
            token['expires_in'] = settings.IMPLICIT_ACCESS_TOKEN_EXPIRES_SECONDS

        if request.grant_type == 'client_credentials':
            request.user = None

        access_token = AccessToken(
            user=request.user,
            scope=token['scope'],
            expires=expires,
            token=token['access_token'],
            application=request.client)
        access_token.save()

        if 'refresh_token' in token:
            refresh_token = RefreshToken(
                user=request.user,
                token=token['refresh_token'],
                application=request.client,
            )
            if request.grant_type == 'authorization_code':
                refresh_tokens = RefreshToken.objects.all().filter(user=request.user,
                                                                   application=request.client).order_by('-id')
                if len(refresh_tokens) > 0:
                    refresh_token = refresh_tokens[0]
                    # Delete the old access_token
                    refresh_token.access_token.delete()
                    if len(refresh_tokens) > 1:
                        # Enforce 1 token pair. Delete all old refresh_tokens
                        RefreshToken.objects.exclude(pk=refresh_token.id).delete()

            refresh_token.access_token = access_token
            refresh_token.save()
            token['refresh_token'] = refresh_token.token
