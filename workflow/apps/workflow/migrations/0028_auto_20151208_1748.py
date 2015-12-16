# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0027_auto_20151208_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='disabled',
            field=models.IntegerField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='workflow',
            name='failed',
            field=models.IntegerField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='workflow',
            name='success',
            field=models.IntegerField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='workflow',
            name='untested',
            field=models.IntegerField(null=True, editable=False),
        ),
    ]
