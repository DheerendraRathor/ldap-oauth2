from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from application.models import Application
from core.utils import SORTED_DISCIPLINES, DEGREES, HOSTELS


def validate_join_year(value):
    current_year = timezone.now().year
    if value < 1958:
        raise ValidationError(_('%d! Are you kidding me? IITB was not even there back then!' % value))
    if value > current_year:
        raise ValidationError(_('Welcome kiddo, welcome to IITB in future!'))


def validate_graduation_year(value):
    current_year = timezone.now().year
    if value < 1958:
        raise ValidationError(_('%d! Are you kidding me? IITB was not even there back then!' % value))
    if value > (current_year + 6):
        raise ValidationError(_('Please enter your expected graduation year'))


class InstituteAddress(models.Model):

    user = models.OneToOneField(User, related_name='insti_address')
    room = models.CharField(max_length=8, null=True, blank=True)
    hostel = models.CharField(max_length=8, choices=HOSTELS, null=True, blank=True)

    def __unicode__(self):
        if self.hostel:
            if self.room:
                return "%s-%s" % (self.hostel, self.room)
            return self.hostel
        return ''


class Program(models.Model):

    user = models.OneToOneField(User, related_name='program')
    department = models.CharField(max_length=16, choices=SORTED_DISCIPLINES, null=True, blank=True)
    join_year = models.PositiveSmallIntegerField(null=True, blank=True, validators=[validate_join_year])
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True, validators=[validate_graduation_year])
    degree = models.CharField(max_length=16, choices=DEGREES, null=True, blank=True)

    def __unicode__(self):
        return "%s, %s" % (self.degree, self.department)


class ContactNumber(models.Model):
    user = models.ForeignKey(User, related_name='contacts')
    number = models.CharField(max_length=16)

    def __unicode__(self):
        return self.number


class SecondaryEmail(models.Model):
    user = models.ForeignKey(User, related_name='secondary_emails')
    email = models.EmailField()

    def __unicode__(self):
        return self.email


class SentMessage(models.Model):
    message_id = models.CharField(max_length=256)
    sender = models.ForeignKey(Application)
    user = models.ForeignKey(User)
    status = models.BooleanField(default=True)
    error_message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message_id
