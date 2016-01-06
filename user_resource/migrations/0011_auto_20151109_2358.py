# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_resource', '0010_historicalcontactnumber_historicalinstituteaddress_historicalprogram_historicalsecondaryemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinstituteaddress',
            name='hostel',
            field=models.CharField(blank=True, max_length=8, null=True, choices=[[b'1', b'Hostel 1'], [b'2', b'Hostel 2'], [b'3', b'Hostel 3'], [b'4', b'Hostel 4'], [b'5', b'Hostel 5'], [b'6', b'Hostel 6'], [b'7', b'Hostel 7'], [b'8', b'Hostel 8'], [b'9', b'Hostel 9'], [b'10', b'Hostel 10'], [b'11', b'Hostel 11'], [b'12', b'Hostel 12'], [b'13', b'Hostel 13'], [b'14', b'Hostel 14'], [b'15', b'Hostel 15'], [b'16', b'Hostel 16'], [b'tansa', b'Tansa'], [b'qip', b'QIP']]),
        ),
        migrations.AlterField(
            model_name='instituteaddress',
            name='hostel',
            field=models.CharField(blank=True, max_length=8, null=True, choices=[[b'1', b'Hostel 1'], [b'2', b'Hostel 2'], [b'3', b'Hostel 3'], [b'4', b'Hostel 4'], [b'5', b'Hostel 5'], [b'6', b'Hostel 6'], [b'7', b'Hostel 7'], [b'8', b'Hostel 8'], [b'9', b'Hostel 9'], [b'10', b'Hostel 10'], [b'11', b'Hostel 11'], [b'12', b'Hostel 12'], [b'13', b'Hostel 13'], [b'14', b'Hostel 14'], [b'15', b'Hostel 15'], [b'16', b'Hostel 16'], [b'tansa', b'Tansa'], [b'qip', b'QIP']]),
        ),
    ]
