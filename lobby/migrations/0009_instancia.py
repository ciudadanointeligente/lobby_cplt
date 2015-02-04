# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popolo', '__first__'),
        ('lobby', '0008_audiencia_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instancia',
            fields=[
                ('organization_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='popolo.Organization')),
                ('rut', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
            bases=('popolo.organization',),
        ),
    ]
