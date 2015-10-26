# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import oauth2_provider.validators
import oauth2_provider.generators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0005_auto_20151013_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalApplication',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('client_id', models.CharField(default=oauth2_provider.generators.generate_client_id, max_length=100, db_index=True)),
                ('redirect_uris', models.TextField(help_text='Allowed URIs list, space separated', blank=True, validators=[oauth2_provider.validators.validate_uris])),
                ('client_type', models.CharField(max_length=32, choices=[('confidential', 'Confidential'), ('public', 'Public')])),
                ('authorization_grant_type', models.CharField(max_length=32, choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials')])),
                ('client_secret', models.CharField(default=oauth2_provider.generators.generate_client_secret, max_length=255, db_index=True, blank=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('skip_authorization', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('logo', models.TextField(max_length=100, null=True, blank=True)),
                ('is_anonymous', models.BooleanField(default=False, help_text=b'Valid for complete anonymous apps. Requires admin permission')),
                ('required_scopes', models.CharField(help_text=b'Default non-tracking permissions. Valid only if application is anonymous', max_length=256, null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('privacy_policy', models.URLField(help_text=b'Link of privacy policy of application', null=True, blank=True)),
                ('created_on', models.DateTimeField(editable=False, blank=True)),
                ('modified_on', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical application',
            },
        ),
    ]
