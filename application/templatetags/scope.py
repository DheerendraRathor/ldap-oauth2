from django import template

from core.utils import get_default_scopes

register = template.Library()


@register.filter(name='zip')
def zip_list(lis1, lis2):
    """
    Template tag to zip 2 lists
    :param lis1: First List
    :param lis2: Second List
    :return: Zipped lists
    """
    return zip(lis1, lis2)


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
