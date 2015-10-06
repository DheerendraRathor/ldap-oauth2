__author__ = 'dheerendra'

from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    def get_default_scopes(self, client_id, request, *args, **kwargs):
        return ['basic']

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        if 'basic' not in request.scopes:
            request.scopes.append('basic')
        return super(CustomOAuth2Validator, self).validate_scopes(client_id, scopes, client, request, *args, **kwargs)
