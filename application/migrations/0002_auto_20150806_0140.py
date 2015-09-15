# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import application.models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='logo',
            field=models.ImageField(null=True, upload_to=application.models.application_logo, blank=True),
        ),
    ]
