# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0009_instancia'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Instancia',
            new_name='Entidad',
        ),
    ]
