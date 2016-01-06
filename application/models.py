import os
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from oauth2_provider.models import AbstractApplication, AccessToken
from simple_history.models import HistoricalRecords

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


def application_logo(instance, filename):  # pylint: disable=unused-argument
    filename = filename.split('.')
    if len(filename) > 1:
        ext = filename[-1]
    else:
        ext = "png"
    return os.path.join("app_logo", uuid4().hex + "." + ext)


@python_2_unicode_compatible
class Application(AbstractApplication):
    """
    Extended oauth2_provider.models.AbstractApplication to include application description and logo
    """
    description = models.TextField()
    logo = models.ImageField(upload_to=application_logo, blank=True, null=True)
    is_anonymous = models.BooleanField(default=False,
                                       help_text='Valid for complete anonymous apps. Requires admin permission')
    required_scopes = models.CharField(max_length=256,
                                       help_text='Default non-tracking permissions. '
                                                 'Valid only if application is anonymous', null=True, blank=True)
    private_scopes = models.CharField(max_length=256, help_text='Private API scopes', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    privacy_policy = models.URLField(null=True, blank=True, help_text='Link of privacy policy of application')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    _history_ = HistoricalRecords()

    def get_logo_url(self):
        try:
            url = self.logo.url
            url = urljoin(settings.MEDIA_URL, url)
        except ValueError:
            url = None
        return url

    def get_absolute_url(self):
        return reverse('oauth2_provider:detail', args=[str(self.id)])

    def clean(self):
        super(Application, self).clean()
        if self.authorization_grant_type == AbstractApplication.GRANT_PASSWORD:
            error = _("Resource owner password based grants are not allowed for now")
            raise ValidationError(error)

    def get_user_count(self):
        return AccessToken.objects.all().filter(application=self).values_list('user', flat=True).distinct().count()

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.client_id
