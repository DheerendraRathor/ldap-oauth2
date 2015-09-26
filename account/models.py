from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField(null=True, blank=True)
    roll_number = models.CharField(max_length=16, null=True, blank=True)
    type = models.CharField(max_length=5, null=True, blank=True)
    mobile = models.CharField(max_length=16, null=True, blank=True)
    is_alumni = models.BooleanField(default=False)
