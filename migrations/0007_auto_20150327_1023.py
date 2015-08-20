# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0006_auto_20150327_0047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='people',
            options={'permissions': (('view_people', 'Can view people'), ('modify_people', 'Can create, edit, and delete people'))},
        ),
        migrations.AlterModelOptions(
            name='program',
            options={'permissions': (('modify_program', 'Can create, edit, and delete programs'),)},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('view_project', 'Can view projects'), ('modify_project', 'Can create, edit, and delete projects'))},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'permissions': (('view_task', 'Can view tasks'), ('modify_task', 'Can create, edit, and delete tasks'))},
        ),
    ]
