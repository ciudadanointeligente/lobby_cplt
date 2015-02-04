# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popolo', '__first__'),
        ('lobby', '0010_auto_20150204_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiencia',
            name='registering_organization',
            field=models.ForeignKey(default=None, to='popolo.Organization'),
            preserve_default=False,
        ),
    ]
