# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('group', models.ForeignKey(to='pm.Group')),
            ],
            options={
            },
            bases=(models.Model,),
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
            options={
            },
            bases=(models.Model,),
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
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskWorker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task', models.ForeignKey(to='pm.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('date_complete', models.DateField()),
                ('percent_committed', models.IntegerField()),
                ('owner', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='pm.People')),
                ('project', models.ForeignKey(to='pm.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='taskworker',
            name='worker',
            field=models.ForeignKey(to='pm.Worker'),
            preserve_default=True,
        ),
    ]
