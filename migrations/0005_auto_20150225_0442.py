# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0004_auto_20141124_0414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blocked_task', models.ForeignKey(related_name=b'blocked_task', to='pm.Task')),
                ('blocking_task', models.ForeignKey(related_name=b'blocking_task', to='pm.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='taskdependency',
            unique_together=set([('blocking_task', 'blocked_task')]),
        ),
        migrations.AddField(
            model_name='project',
            name='priority',
            field=models.CharField(default=b'ST', max_length=2, null=True, choices=[(b'HI', b'High'), (b'ST', b'Standard'), (b'LO', b'Low')]),
            preserve_default=True,
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
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Active'), (b'O', b'On hold'), (b'W', b'Warranty'), (b'M', b'Maintenance'), (b'C', b'Completed')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(default=b'Q', max_length=1, choices=[(b'Q', b'Queued'), (b'A', b'Active'), (b'O', b'On hold'), (b'W', b'Waiting on customer'), (b'C', b'Completed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='requester',
            field=models.ForeignKey(related_name=b'person_requester', to='pm.People'),
        ),
    ]
