# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0004_audiencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiencia',
            name='date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='audiencia',
            name='length',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='audiencia',
            name='observations',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='audiencia',
            name='place',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
