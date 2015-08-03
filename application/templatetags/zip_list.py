__author__ = 'dheerendra'

from django import template

register = template.Library()

@register.filter(name='zip')
def zip_list(a,b):
    return list(zip(a, b))