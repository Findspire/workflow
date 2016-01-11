# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0031_itemcategory_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='categories',
        ),
    ]
