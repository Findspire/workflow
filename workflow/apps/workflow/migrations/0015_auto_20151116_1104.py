# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0014_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(db_index=True, max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='itemcategory',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Name', db_index=True),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name', db_index=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Name', db_index=True),
        ),
    ]
