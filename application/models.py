from django.db import models
from oauth2_provider.models import AbstractApplication
from uuid import uuid4
import os
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

def application_logo(instance, filename):
    filename = filename.split('.')
    if len(filename) > 1:
        ext = filename[-1]
    else:
        ext = "jpg"
    return os.path.join("app_logo", uuid4().hex + "." + ext)

class Application(AbstractApplication):

    description = models.TextField()
    logo = models.ImageField(upload_to=application_logo, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('oauth:detail', args=[str(self.id)])

    def clean(self):
        super(Application, self).clean()
        if self.authorization_grant_type == AbstractApplication.GRANT_PASSWORD:
            error = _("Resource owner password based grants are not allowed for now")
            raise ValidationError(error)


