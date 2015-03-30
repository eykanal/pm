# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0007_auto_20150327_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='boss',
            field=models.ForeignKey(related_name='boss_of', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
