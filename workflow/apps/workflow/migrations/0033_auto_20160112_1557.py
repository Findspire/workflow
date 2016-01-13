# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0032_remove_project_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemcategory',
            options={'ordering': ['position']},
        ),
    ]
