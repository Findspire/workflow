# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0028_auto_20151208_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='disabled',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='failed',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='success',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='untested',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
