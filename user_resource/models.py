from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from application.models import Application


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
    HOSTEL_CHOICES = [
        ['1', 'Hostel 1'],
        ['2', 'Hostel 2'],
        ['3', 'Hostel 3'],
        ['4', 'Hostel 4'],
        ['5', 'Hostel 5'],
        ['6', 'Hostel 6'],
        ['7', 'Hostel 7'],
        ['8', 'Hostel 8'],
        ['9', 'Hostel 9'],
        ['10', 'Hostel 10'],
        ['10A', 'Hostel 10A'],
        ['11', 'Hostel 11'],
        ['12', 'Hostel 12'],
        ['13', 'Hostel 13'],
        ['14', 'Hostel 14'],
        ['15', 'Hostel 15'],
        ['16', 'Hostel 16'],
        ['tansa', 'Tansa'],
        ['qip', 'QIP'],
    ]

    user = models.OneToOneField(User, related_name='insti_address')
    room = models.CharField(max_length=8, null=True, blank=True)
    hostel = models.CharField(max_length=8, choices=HOSTEL_CHOICES, null=True, blank=True)


class Program(models.Model):
    DEPARTMENT_CHOICES = [
        ['AE', 'Aerospace Engineering'],
        ['BB', 'Biosciences and Bioengineering'],
        ['CHE', 'Chemical Engineering'],
        ['CH', 'Chemistry'],
        ['CLE', 'Civil Engineering'],
        ['CSE', 'Computer Science & Engineering'],
        ['ES', 'Earth Sciences'],
        ['EE', 'Electrical Engineering'],
        ['ESE', 'Energy Science and Engineering'],
        ['HSS', 'Humanities & Social Science'],
        ['IDC', 'Industrial Design Centre'],
        ['MM', 'Mathematics'],
        ['ME', 'Mechanical Engineering'],
        ['MEMS', 'Metallurgical Engineering & Materials Science'],
        ['PH', 'Physics'],
    ]

    DEGREES = [
        ['BTECH', 'Bachelor of Technology'],
        ['MTECH', 'Master of Technology'],
        ['DD', 'Dual Degree'],
        ['MSC', 'Master of Science'],
        ['PHD', 'PhD'],
        ['MDES', 'Master of Design'],
        ['MPHIL', 'Master of Philosophy'],
        ['MMG', 'Master of Management'],
    ]

    user = models.OneToOneField(User, related_name='program')
    department = models.CharField(max_length=8, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    join_year = models.PositiveSmallIntegerField(null=True, blank=True, validators=[validate_join_year])
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True, validators=[validate_graduation_year])
    degree = models.CharField(max_length=6, choices=DEGREES)


class ContactNumber(models.Model):
    user = models.ForeignKey(User, related_name='contacts')
    number = models.CharField(max_length=16)


class SecondaryEmail(models.Model):
    user = models.ForeignKey(User, related_name='secondary_emails')
    email = models.EmailField()


class SentMessage(models.Model):
    message_id = models.CharField(max_length=256)
    sender = models.ForeignKey(Application)
    user = models.ForeignKey(User)
    status = models.BooleanField(default=True)
    error_message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
