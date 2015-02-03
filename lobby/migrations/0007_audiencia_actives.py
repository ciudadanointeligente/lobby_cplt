# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0006_audiencia_passive'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiencia',
            name='actives',
            field=models.ManyToManyField(to='lobby.Active'),
            preserve_default=True,
        ),
    ]
