# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def default_program(apps, schema_editor):
    Program = apps.get_model("pm", "Program")
    Program.objects.create(name="None", description="Default program for projects.")

# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# pm.migrations.0011_auto_20150406_0246

class Migration(migrations.Migration):

    replaces = [(b'pm', '0001_initial'), (b'pm', '0002_auto_20141121_0615'), (b'pm', '0003_auto_20141123_2048'), (b'pm', '0004_auto_20141124_0414'), (b'pm', '0005_auto_20150225_0442'), (b'pm', '0006_auto_20150327_0047'), (b'pm', '0007_auto_20150327_1023'), (b'pm', '0008_auto_20150330_0152'), (b'pm', '0009_auto_20150401_0120'), (b'pm', '0010_group_internal'), (b'pm', '0011_auto_20150406_0246'), (b'pm', '0012_auto_20150503_0315')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('group', models.ForeignKey(to='pm.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('requester', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('due_date', models.DateField()),
                ('date_complete', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('due_date', models.DateField()),
                ('date_complete', models.DateField()),
                ('project', models.ForeignKey(to='pm.Project')),
            ],
        ),
        migrations.CreateModel(
            name='TaskWorker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task', models.ForeignKey(to='pm.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('date_complete', models.DateField(null=True, blank=True)),
                ('percent_committed', models.IntegerField(null=True, blank=True)),
                ('owner', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='pm.People')),
                ('project', models.ForeignKey(to='pm.Project')),
            ],
        ),
        migrations.AddField(
            model_name='taskworker',
            name='worker',
            field=models.ForeignKey(to='pm.Worker'),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_complete',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_complete',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(null=True),
        ),
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
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blocked_task', models.ForeignKey(related_name=b'blocked_task', to='pm.Task')),
                ('blocking_task', models.ForeignKey(related_name=b'blocking_task', to='pm.Task')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='taskdependency',
            unique_together=set([('blocking_task', 'blocked_task')]),
        ),
        migrations.AddField(
            model_name='project',
            name='priority',
            field=models.CharField(default=b'ST', max_length=2, null=True, choices=[(b'HI', b'High'), (b'ST', b'Standard'), (b'LO', b'Low')]),
        ),
        migrations.AddField(
            model_name='project',
            name='program',
            field=models.ForeignKey(default='', to='pm.Program'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='project_manager',
            field=models.ForeignKey(related_name=b'person_project_manager', default='', to='pm.People'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='sharepoint_ticket',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Active'), (b'O', b'On hold'), (b'W', b'Warranty'), (b'M', b'Maintenance'), (b'C', b'Completed')]),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(default=b'Q', max_length=1, choices=[(b'Q', b'Queued'), (b'A', b'Active'), (b'O', b'On hold'), (b'W', b'Waiting on customer'), (b'C', b'Completed')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='requester',
            field=models.ForeignKey(related_name=b'person_requester', to='pm.People'),
        ),
        migrations.AddField(
            model_name='people',
            name='boss',
            field=models.OneToOneField(related_name='boss_of', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='people',
            name='name',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
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
        migrations.RemoveField(
            model_name='people',
            name='boss',
        ),
        migrations.AddField(
            model_name='group',
            name='manager',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='internal',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(
            code=default_program,
        ),
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
        migrations.AddField(
            model_name='task',
            name='status_on_hold',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='status_waiting',
            field=models.BooleanField(default=False),
        ),
    ]
