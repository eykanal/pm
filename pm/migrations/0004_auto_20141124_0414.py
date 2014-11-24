# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0003_auto_20141123_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='id',
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=200, serialize=False, primary_key=True),
        ),
        migrations.AlterUniqueTogether(
            name='people',
            unique_together=set([('name', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('name', 'project')]),
        ),
        migrations.AlterUniqueTogether(
            name='taskworker',
            unique_together=set([('task', 'worker')]),
        ),
        migrations.AlterUniqueTogether(
            name='worker',
            unique_together=set([('project', 'person')]),
        ),
    ]
