# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0006_userprofile_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalUserProfile',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('profile_picture', models.TextField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('roll_number', models.CharField(max_length=16, null=True, blank=True)),
                ('type', models.CharField(max_length=16, null=True, blank=True)),
                ('mobile', models.CharField(max_length=16, null=True, blank=True)),
                ('is_alumni', models.BooleanField(default=False)),
                ('sex', models.CharField(blank=True, max_length=10, null=True, choices=[(b'male', b'Male'), (b'female', b'Female'), (b'other', b'Other')])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical user profile',
            },
        ),
    ]
