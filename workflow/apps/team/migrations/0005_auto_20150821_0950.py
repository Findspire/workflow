# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_auto_20150807_0844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='skill',
            options={'verbose_name': 'Skill instance', 'verbose_name_plural': 'Skill instances'},
        ),
        migrations.AlterModelOptions(
            name='skillcategory',
            options={'verbose_name': 'Skill category', 'verbose_name_plural': 'Skill categories'},
        ),
        migrations.AlterModelOptions(
            name='skillsubject',
            options={'verbose_name': 'Skill subject', 'verbose_name_plural': 'Skill subjects'},
        ),
        migrations.AlterField(
            model_name='person',
            name='arrival_date',
            field=models.DateField(verbose_name='Arrival date'),
        ),
        migrations.AlterField(
            model_name='person',
            name='contract_type',
            field=models.SmallIntegerField(default=0, verbose_name='Contract', choices=[(0, 'Permanent contract'), (1, 'Fixed-term contract'), (3, 'Internship'), (4, 'Freelance')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='skill',
            name='person',
            field=models.ForeignKey(verbose_name='Person', to='team.Person'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='strength',
            field=models.IntegerField(verbose_name='Strength'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='techno',
            field=models.ForeignKey(verbose_name='Skill subject', to='team.SkillSubject'),
        ),
        migrations.AlterField(
            model_name='skillcategory',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='skillsubject',
            name='category',
            field=models.ForeignKey(verbose_name='Category', to='team.SkillCategory'),
        ),
        migrations.AlterField(
            model_name='skillsubject',
            name='description',
            field=models.CharField(max_length=1024, null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='skillsubject',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(related_name='leader', verbose_name='Leader', to='team.Person'),
        ),
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='members', verbose_name='Members', to='team.Person'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Name'),
        ),
    ]
