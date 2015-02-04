# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0011_audiencia_registering_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiencia',
            name='registering_organization',
            field=models.ForeignKey(to='popolo.Organization', null=True),
            preserve_default=True,
        ),
    ]
