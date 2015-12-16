# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0026_remove_workflow_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workflow',
            old_name='version',
            new_name='name',
        ),
    ]
