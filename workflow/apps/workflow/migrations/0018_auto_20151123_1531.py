# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0017_item_assigned_to_name_cache'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['position']},
        ),
        migrations.AlterField(
            model_name='itemcategory',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Name'),
        ),
    ]
