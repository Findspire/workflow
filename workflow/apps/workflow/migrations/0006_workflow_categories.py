# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0005_auto_20150821_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='categories',
            field=models.ManyToManyField(to='workflow.ItemCategory', verbose_name='Categories', blank=True),
        ),
    ]
