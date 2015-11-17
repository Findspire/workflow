# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0016_item_comments_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='assigned_to_name_cache',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
