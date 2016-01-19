# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0034_changelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='changelog',
            name='created_at',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
