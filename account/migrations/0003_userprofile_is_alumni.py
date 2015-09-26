# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150926_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_alumni',
            field=models.BooleanField(default=False),
        ),
    ]
