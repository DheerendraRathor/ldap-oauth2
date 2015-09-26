# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import user_resource.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_resource', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactnumber',
            name='is_primary',
        ),
        migrations.RemoveField(
            model_name='program',
            name='roll_number',
        ),
        migrations.AddField(
            model_name='program',
            name='degree',
            field=models.CharField(default='BTECH', max_length=6, choices=[[b'BTECH', b'Bachelor of Technology'], [b'MTECH', b'Master of Technology'], [b'DD', b'Dual Degree'], [b'MSC', b'Master of Science'], [b'PHD', b'PhD'], [b'MDES', b'Master of Design'], [b'MPHIL', b'Master of Philosophy'], [b'MMG', b'Master of Management']]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='instituteaddress',
            name='hostel',
            field=models.CharField(blank=True, max_length=8, null=True, choices=[[b'1', b'Hostel 1'], [b'2', b'Hostel 2'], [b'3', b'Hostel 3'], [b'4', b'Hostel 4'], [b'5', b'Hostel 5'], [b'6', b'Hostel 6'], [b'7', b'Hostel 7'], [b'8', b'Hostel 8'], [b'9', b'Hostel 9'], [b'10', b'Hostel 10'], [b'11', b'Hostel 11'], [b'12', b'Hostel 12'], [b'13', b'Hostel 13'], [b'14', b'Hostel 14'], [b'15', b'Hostel 15'], [b'16', b'Hostel 16'], [b'tansa', b'Tansa'], [b'qip', b'QIP']]),
        ),
        migrations.AlterField(
            model_name='instituteaddress',
            name='room',
            field=models.CharField(max_length=8, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='graduation_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[user_resource.models.validate_graduation_year]),
        ),
        migrations.AlterField(
            model_name='program',
            name='join_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[user_resource.models.validate_join_year]),
        ),
    ]
