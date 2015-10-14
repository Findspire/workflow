# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0009_item_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='order',
            new_name='position',
        ),
    ]
