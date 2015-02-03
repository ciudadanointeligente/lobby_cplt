# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0003_auto_20150203_1835'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audiencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
