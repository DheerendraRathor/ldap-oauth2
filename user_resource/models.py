from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords

from application.models import Application
from core.utils import DEGREES, HOSTELS, HOSTELS_WITH_WINGS, ROOM_VALIDATION_REGEX, SORTED_DISCIPLINES


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


@python_2_unicode_compatible
class InstituteAddress(models.Model):
    user = models.OneToOneField(User, related_name='insti_address')
    room = models.CharField(max_length=8, null=True, blank=True)
    hostel = models.CharField(max_length=8, choices=HOSTELS, null=True, blank=True)
    _history_ = HistoricalRecords()

    def clean(self):
        if self.room:
            if self.hostel in HOSTELS_WITH_WINGS:
                if not ROOM_VALIDATION_REGEX.match(self.room):
                    raise ValidationError(_('Room number must have wing name like A-123'))

    def __str__(self):
        if self.hostel:
            if self.room:
                return "%s-%s" % (self.hostel, self.room)
            return self.hostel
        return ''


@python_2_unicode_compatible
class Program(models.Model):
    user = models.OneToOneField(User, related_name='program')
    department = models.CharField(max_length=16, choices=SORTED_DISCIPLINES, null=True, blank=True)
    join_year = models.PositiveSmallIntegerField(null=True, blank=True, validators=[validate_join_year])
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True, validators=[validate_graduation_year])
    degree = models.CharField(max_length=16, choices=DEGREES, null=True, blank=True)
    _history_ = HistoricalRecords()

    def __str__(self):
        return "%s, %s" % (self.get_degree_display(), self.get_department_display())


@python_2_unicode_compatible
class ContactNumber(models.Model):
    user = models.ForeignKey(User, related_name='contacts')
    number = models.CharField(max_length=16)
    _history_ = HistoricalRecords()

    def __str__(self):
        return self.number


@python_2_unicode_compatible
class SecondaryEmail(models.Model):
    user = models.ForeignKey(User, related_name='secondary_emails')
    email = models.EmailField()
    _history_ = HistoricalRecords()

    def __str__(self):
        return self.email


@python_2_unicode_compatible
class SentMessage(models.Model):
    message_id = models.CharField(max_length=256)
    sender = models.ForeignKey(Application)
    user = models.ForeignKey(User)
    status = models.BooleanField(default=True)
    error_message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message_id
