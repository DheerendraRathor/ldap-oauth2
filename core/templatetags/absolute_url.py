from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_url(context, location):
    request = context['request']
    return request.build_absolute_uri(location)
