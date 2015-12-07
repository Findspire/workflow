# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0021_auto_20151201_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='position',
            field=models.IntegerField(null=True, editable=False),
        ),
    ]
