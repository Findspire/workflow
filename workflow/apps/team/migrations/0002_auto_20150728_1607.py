# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competencecategory',
            options={'verbose_name': 'competence category', 'verbose_name_plural': 'competence categories'},
        ),
        migrations.AlterModelOptions(
            name='competenceinstance',
            options={'verbose_name': 'competence instance', 'verbose_name_plural': 'competence instances'},
        ),
        migrations.AlterModelOptions(
            name='competencesubject',
            options={'verbose_name': 'competence subject', 'verbose_name_plural': 'competence subjects'},
        ),
    ]
