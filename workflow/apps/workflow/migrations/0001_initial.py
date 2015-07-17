# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentInstanceItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('comments', models.TextField(max_length=1000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompetencesSubject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompetencesSubjectCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CompetencesType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('strength', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=512)),
                ('details', models.TextField(max_length=1000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('firstname', models.CharField(max_length=64)),
                ('lastname', models.CharField(max_length=64)),
                ('arrival_date', models.DateField()),
                ('departure_date', models.DateField(null=True, blank=True)),
                ('access_card', models.CharField(max_length=64, null=True, blank=True)),
                ('token_serial', models.CharField(max_length=32, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=32, null=True, blank=True)),
                ('contract_type', models.ForeignKey(to='workflow.ContractType')),
                ('django_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('leader', models.ForeignKey(to='workflow.Person')),
            ],
        ),
        migrations.CreateModel(
            name='TeamPerson',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('person', models.ForeignKey(to='workflow.Person')),
                ('team', models.ForeignKey(to='workflow.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('leaders', models.ManyToManyField(to='workflow.Person')),
                ('teams', models.ManyToManyField(to='workflow.Team')),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('workflow', models.ForeignKey(to='workflow.Workflow')),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowInstance',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('creation_date', models.DateField(auto_now=True)),
                ('version', models.CharField(max_length=128)),
                ('workflow', models.ForeignKey(to='workflow.Workflow')),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowInstanceItems',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('assigned_to', models.ForeignKey(blank=True, to='workflow.Person', null=True)),
                ('item', models.ForeignKey(to='workflow.Item')),
                ('validation', models.ForeignKey(to='workflow.Validation', null=True)),
                ('workflowinstance', models.ForeignKey(to='workflow.WorkflowInstance')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='workflow_category',
            field=models.ForeignKey(to='workflow.WorkflowCategory'),
        ),
        migrations.AddField(
            model_name='competencessubjectcategory',
            name='part_of_team',
            field=models.ForeignKey(to='workflow.Team'),
        ),
        migrations.AddField(
            model_name='competencessubject',
            name='competence_subject_category',
            field=models.ForeignKey(to='workflow.CompetencesSubjectCategory'),
        ),
        migrations.AddField(
            model_name='competence',
            name='competence_subject',
            field=models.ForeignKey(to='workflow.CompetencesSubject'),
        ),
        migrations.AddField(
            model_name='competence',
            name='comptype',
            field=models.ForeignKey(related_name='comptype', to='workflow.CompetencesType', null=True),
        ),
        migrations.AddField(
            model_name='competence',
            name='person',
            field=models.ForeignKey(to='workflow.Person'),
        ),
        migrations.AddField(
            model_name='competence',
            name='target_comptype',
            field=models.ForeignKey(to='workflow.CompetencesType', null=True),
        ),
        migrations.AddField(
            model_name='commentinstanceitem',
            name='item',
            field=models.ForeignKey(to='workflow.WorkflowInstanceItems'),
        ),
        migrations.AddField(
            model_name='commentinstanceitem',
            name='person',
            field=models.ForeignKey(blank=True, to='workflow.Person', null=True),
        ),
    ]
