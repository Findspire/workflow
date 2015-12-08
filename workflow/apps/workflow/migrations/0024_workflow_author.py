# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0005_auto_20150821_0950'),
        ('workflow', '0023_auto_20151207_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='author',
            field=models.ForeignKey(editable=False, to='team.Person', null=True),
        ),
    ]
