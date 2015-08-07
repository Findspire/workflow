# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_rename_models'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='access_card',
        ),
        migrations.RemoveField(
            model_name='person',
            name='departure_date',
        ),
        migrations.RemoveField(
            model_name='person',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='person',
            name='token_serial',
        ),
        migrations.AlterField(
            model_name='person',
            name='contract_type',
            field=models.SmallIntegerField(default=0, choices=[(0, 'Permanent contract'), (1, 'Fixed-term contract'), (3, 'Internship'), (4, 'Freelance')]),
        ),
        migrations.AlterModelOptions(
            name='skillcategory',
            options={'verbose_name': 'skill category', 'verbose_name_plural': 'skill categories'},
        ),
        migrations.AlterModelOptions(
            name='skillsubject',
            options={'verbose_name': 'skill subject', 'verbose_name_plural': 'skill subjects'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'verbose_name': 'skill instance', 'verbose_name_plural': 'skill instances'},
        ),
        migrations.DeleteModel(
            name='ContractType',
        ),
    ]
