# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0005_auto_20150203_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiencia',
            name='passive',
            field=models.ForeignKey(default=None, to='lobby.Passive'),
            preserve_default=False,
        ),
    ]
