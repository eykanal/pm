# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0011_auto_20150406_0246'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectReviews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='pm.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.SmallIntegerField()),
                ('comments', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkerReviews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review', models.ForeignKey(to='pm.Reviews')),
                ('worker', models.ForeignKey(to='pm.Worker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='workerreviews',
            unique_together=set([('review', 'worker')]),
        ),
        migrations.AddField(
            model_name='projectreviews',
            name='review',
            field=models.ForeignKey(to='pm.Reviews'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='projectreviews',
            unique_together=set([('review', 'project')]),
        ),
    ]
