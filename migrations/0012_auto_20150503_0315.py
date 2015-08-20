# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0011_auto_20150406_0246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
        migrations.AddField(
            model_name='task',
            name='status_on_hold',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='status_waiting',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
