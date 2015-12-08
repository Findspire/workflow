# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0024_workflow_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow',
            name='private',
        ),
    ]
