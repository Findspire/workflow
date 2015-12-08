# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0025_remove_workflow_private'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow',
            name='author',
        ),
    ]
