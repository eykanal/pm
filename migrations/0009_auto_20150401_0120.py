# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pm', '0008_auto_20150330_0152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people',
            name='boss',
        ),
        migrations.AddField(
            model_name='group',
            name='manager',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
