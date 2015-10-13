from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='zip')
def zip_list(a, b):
    return list(zip(a, b))


@register.filter(name='get_basic_scope')
def get_basic_scope(zipped_scope_description):
    return [(scope, description) for scope, description in zipped_scope_description if
            scope in settings.OAUTH2_DEFAULT_SCOPES]


@register.filter(name='remove_basic_scope')
def remove_basic_scope(zipped_scope_description):
    return [(scope, description) for scope, description in zipped_scope_description if
            scope not in settings.OAUTH2_DEFAULT_SCOPES]
