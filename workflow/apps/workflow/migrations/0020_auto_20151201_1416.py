# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0019_auto_20151201_1411'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workflow',
            old_name='archive',
            new_name='archived',
        ),
    ]
