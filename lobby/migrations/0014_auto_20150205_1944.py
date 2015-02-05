# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0013_auto_20150205_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiencia',
            name='passive',
            field=models.ForeignKey(to='lobby.Passive', null=True),
            preserve_default=True,
        ),
    ]
