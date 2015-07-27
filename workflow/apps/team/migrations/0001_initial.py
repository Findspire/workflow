# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetenceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CompetenceInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('strength', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CompetenceSubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
                ('category', models.ForeignKey(to='team.CompetenceCategory')),
            ],
        ),
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arrival_date', models.DateField()),
                ('departure_date', models.DateField(null=True, blank=True)),
                ('access_card', models.CharField(max_length=64, null=True, blank=True)),
                ('token_serial', models.CharField(max_length=32, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=32, null=True, blank=True)),
                ('contract_type', models.ForeignKey(to='team.ContractType')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('leader', models.ForeignKey(related_name='leader', to='team.Person')),
                ('members', models.ManyToManyField(related_name='members', to='team.Person')),
            ],
        ),
        migrations.AddField(
            model_name='competenceinstance',
            name='person',
            field=models.ForeignKey(to='team.Person'),
        ),
        migrations.AddField(
            model_name='competenceinstance',
            name='techno',
            field=models.ForeignKey(to='team.CompetenceSubject'),
        ),
    ]
