from django import template
from django.conf import settings
from core.utils import get_default_scopes

register = template.Library()


@register.filter(name='zip')
def zip_list(a, b):
    return list(zip(a, b))


@register.filter(name='get_basic_scope')
def get_basic_scope(zipped_scope_description, application):
    default_scopes = get_default_scopes(application)
    return [(scope, description) for scope, description in zipped_scope_description if
            scope in default_scopes]


@register.filter(name='remove_basic_scope')
def remove_basic_scope(zipped_scope_description, application):
    default_scopes = get_default_scopes(application)
    return [(scope, description) for scope, description in zipped_scope_description if
            scope not in default_scopes]
