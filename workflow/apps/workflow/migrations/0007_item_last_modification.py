# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0006_workflow_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='last_modification',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
