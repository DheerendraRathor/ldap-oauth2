__author__ = 'dheerendra'

from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        return []
