# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0002_auto_20141121_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='date_complete',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_complete',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='date_complete',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='percent_committed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
