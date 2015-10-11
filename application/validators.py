from datetime import timedelta

from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.models import RefreshToken, AccessToken
from django.utils import timezone
from oauth2_provider.settings import oauth2_settings


class CustomOAuth2Validator(OAuth2Validator):
    def get_default_scopes(self, client_id, request, *args, **kwargs):
        return ['basic']

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        if 'basic' not in request.scopes:
            request.scopes.append('basic')
        return super(CustomOAuth2Validator, self).validate_scopes(client_id, scopes, client, request, *args, **kwargs)

    def save_bearer_token(self, token, request, *args, **kwargs):
        """
        It's messy. It is 90% code from parent function. I didn't find a way to reduce it.
        I tried and I failed :'(
        """

        """
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
                try:
                    refresh_token = RefreshToken.objects.get(user=request.user, application=request.client)
                    refresh_token.access_token.delete()
                    # Deleted the old access_token
                except RefreshToken.DoesNotExist:
                    pass
            refresh_token.access_token = access_token
            refresh_token.save()
            token['refresh_token'] = refresh_token.token

        token['expires_in'] = oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS
