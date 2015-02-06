# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0014_auto_20150205_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='entidad',
            name='remunerado',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
