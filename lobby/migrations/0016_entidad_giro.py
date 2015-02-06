# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0015_entidad_remunerado'),
    ]

    operations = [
        migrations.AddField(
            model_name='entidad',
            name='giro',
            field=models.CharField(default=b'', max_length=1024),
            preserve_default=True,
        ),
    ]
