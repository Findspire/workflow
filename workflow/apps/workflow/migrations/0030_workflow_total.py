# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0029_auto_20151208_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='total',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
