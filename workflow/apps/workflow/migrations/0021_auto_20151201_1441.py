# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0020_auto_20151201_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
