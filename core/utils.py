from django.conf import settings


def get_default_scopes(application):
    if application.is_anonymous:
        return application.required_scopes.split()
    return settings.OAUTH2_DEFAULT_SCOPES
