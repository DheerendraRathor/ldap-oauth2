from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    room = models.CharField(max_length=8)
    hostel = models.CharField(max_length=8, choices=HOSTEL_CHOICES)


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

    CURRENT_YEAR = timezone.now().year

    JOIN_YEAR = [(y,y) for y in range(CURRENT_YEAR, CURRENT_YEAR - 6, -1)]

    GRADUATION_YEAR = [(y,y) for y in range(CURRENT_YEAR, CURRENT_YEAR + 6)]

    user = models.OneToOneField(User, related_name='program')
    roll_number = models.CharField(max_length=16, null=True, blank=True)
    department = models.CharField(max_length=8, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    join_year = models.CharField(max_length=4, choices=JOIN_YEAR, null=True, blank=True)
    graduation_year = models.CharField(max_length=4, choices=GRADUATION_YEAR, null=True, blank=True)


class ContactNumber(models.Model):
    user = models.ForeignKey(User, related_name='contacts')
    number = models.CharField(max_length=16)
    is_primary = models.BooleanField(default=False)


class SecondaryEmail(models.Model):
    user = models.ForeignKey(User, related_name='secondary_emails')
    email = models.EmailField()
