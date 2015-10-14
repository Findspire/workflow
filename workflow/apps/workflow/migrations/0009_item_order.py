# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0008_auto_20151012_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.IntegerField(null=True, editable=False),
        ),
    ]
