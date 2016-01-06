# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_historicalapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='private_scopes',
            field=models.CharField(help_text=b'Private API scopes', max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalapplication',
            name='private_scopes',
            field=models.CharField(help_text=b'Private API scopes', max_length=256, null=True, blank=True),
        ),
    ]
