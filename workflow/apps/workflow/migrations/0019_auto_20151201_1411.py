# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0018_auto_20151123_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='archive',
            field=models.CharField(default=0, max_length=50, choices=[(0, 'No archived'), (1, 'Archived')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
