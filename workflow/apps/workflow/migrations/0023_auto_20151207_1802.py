# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0022_workflow_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workflow',
            options={'ordering': ['position']},
        ),
        migrations.AddField(
            model_name='workflow',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='validation',
            field=models.SmallIntegerField(default=0, verbose_name='Validation', choices=[(0, 'Untested'), (1, 'Success'), (2, 'Failed'), (3, 'Disabled')]),
        ),
    ]
