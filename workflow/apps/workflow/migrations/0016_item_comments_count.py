# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0015_auto_20151116_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='comments_count',
            field=models.IntegerField(null=True, editable=False),
        ),
    ]
