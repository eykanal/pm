# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0009_auto_20150401_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='internal',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
