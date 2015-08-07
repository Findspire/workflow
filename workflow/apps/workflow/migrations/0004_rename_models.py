# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_auto_20150727_0921'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WorkflowInstance',
            new_name='Workflow',
        ),
        migrations.RenameModel(
            old_name='ItemInstance',
            new_name='Item',
        ),
    ]
