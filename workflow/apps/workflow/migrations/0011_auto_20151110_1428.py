# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0010_auto_20151014_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='items',
        ),
        migrations.AddField(
            model_name='project',
            name='categories',
            field=models.ManyToManyField(to='workflow.ItemCategory', verbose_name='Categories', blank=True),
        ),
    ]
