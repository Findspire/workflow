# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0007_item_last_modification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='last_modification',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='item',
            name='updated_at',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
    ]
