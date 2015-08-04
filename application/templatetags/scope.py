__author__ = 'dheerendra'

from django import template

register = template.Library()

@register.filter(name='zip')
def zip_list(a,b):
    return list(zip(a, b))


@register.filter(name='remove_basic_scope')
def remove_basic_scope(a):
    return [(s,d) for s,d in a if s != 'basic']