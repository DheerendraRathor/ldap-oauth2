from django import template
from django.conf import settings

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

register = template.Library()


@register.simple_tag()
def model_field_media_url(field):
    try:
        url = field.url
        url = urljoin(settings.MEDIA_URL, url)
    except ValueError:
        url = None
    return url
