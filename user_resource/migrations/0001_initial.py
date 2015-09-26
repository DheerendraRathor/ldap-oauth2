# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=16)),
                ('is_primary', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='contacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InstituteAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room', models.CharField(max_length=8)),
                ('hostel', models.CharField(max_length=8, choices=[[b'1', b'Hostel 1'], [b'2', b'Hostel 2'], [b'3', b'Hostel 3'], [b'4', b'Hostel 4'], [b'5', b'Hostel 5'], [b'6', b'Hostel 6'], [b'7', b'Hostel 7'], [b'8', b'Hostel 8'], [b'9', b'Hostel 9'], [b'10', b'Hostel 10'], [b'11', b'Hostel 11'], [b'12', b'Hostel 12'], [b'13', b'Hostel 13'], [b'14', b'Hostel 14'], [b'15', b'Hostel 15'], [b'16', b'Hostel 16'], [b'tansa', b'Tansa'], [b'qip', b'QIP']])),
                ('user', models.OneToOneField(related_name='insti_address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roll_number', models.CharField(max_length=16, null=True, blank=True)),
                ('department', models.CharField(blank=True, max_length=8, null=True, choices=[[b'AE', b'Aerospace Engineering'], [b'BB', b'Biosciences and Bioengineering'], [b'CHE', b'Chemical Engineering'], [b'CH', b'Chemistry'], [b'CLE', b'Civil Engineering'], [b'CSE', b'Computer Science & Engineering'], [b'ES', b'Earth Sciences'], [b'EE', b'Electrical Engineering'], [b'ESE', b'Energy Science and Engineering'], [b'HSS', b'Humanities & Social Science'], [b'IDC', b'Industrial Design Centre'], [b'MM', b'Mathematics'], [b'ME', b'Mechanical Engineering'], [b'MEMS', b'Metallurgical Engineering & Materials Science'], [b'PH', b'Physics']])),
                ('join_year', models.PositiveSmallIntegerField(blank=True, max_length=4, null=True, choices=[(2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010)])),
                ('graduation_year', models.PositiveSmallIntegerField(blank=True, max_length=4, null=True, choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020)])),
                ('user', models.OneToOneField(related_name='program', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SecondaryEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(related_name='secondary_emails', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
