# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def default_program(apps, schema_editor):
    Program = apps.get_model("pm", "Program")
    Program.objects.create(name="None", description="Default program for projects.")


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0010_group_internal'),
    ]

    operations = [
        migrations.RunPython(default_program),
    ]
