# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0030_workflow_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcategory',
            name='position',
            field=models.IntegerField(null=True, editable=False),
        ),
    ]
