# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0002_auto_20150723_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competenceinstance',
            name='person',
        ),
        migrations.RemoveField(
            model_name='competenceinstance',
            name='techno',
        ),
        migrations.RemoveField(
            model_name='competencesubject',
            name='category',
        ),
        migrations.RemoveField(
            model_name='person',
            name='contract_type',
        ),
        migrations.RemoveField(
            model_name='person',
            name='user',
        ),
        migrations.RemoveField(
            model_name='team',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
        migrations.AlterField(
            model_name='comment',
            name='person',
            field=models.ForeignKey(to='team.Person'),
        ),
        migrations.AlterField(
            model_name='iteminstance',
            name='assigned_to',
            field=models.ForeignKey(blank=True, to='team.Person', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='team',
            field=models.ForeignKey(to='team.Team'),
        ),
        migrations.DeleteModel(
            name='CompetenceCategory',
        ),
        migrations.DeleteModel(
            name='CompetenceInstance',
        ),
        migrations.DeleteModel(
            name='CompetenceSubject',
        ),
        migrations.DeleteModel(
            name='ContractType',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
