# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_auto_20150728_1607'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CompetenceCategory',
            new_name='SkillCategory',
        ),
        migrations.RenameModel(
            old_name='CompetenceSubject',
            new_name='SkillSubject',
        ),
        migrations.RenameModel(
            old_name='CompetenceInstance',
            new_name='Skill',
        ),
    ]
