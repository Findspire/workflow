# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflow', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('text', models.TextField(max_length=1000)),
            ],
        ),
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
                ('category', models.ForeignKey(to='workflow.CompetenceCategory')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ItemInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('validation', models.SmallIntegerField(default=0, choices=[(0, 'Untested'), (1, 'Success'), (2, 'Failed')])),
            ],
        ),
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=1000, null=True, blank=True)),
                ('category', models.ForeignKey(to='workflow.ItemCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('items', models.ManyToManyField(to='workflow.ItemModel', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='commentinstanceitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='commentinstanceitem',
            name='person',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='competence_subject',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='comptype',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='person',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='target_comptype',
        ),
        migrations.RemoveField(
            model_name='competencessubject',
            name='competence_subject_category',
        ),
        migrations.RemoveField(
            model_name='competencessubjectcategory',
            name='part_of_team',
        ),
        migrations.RemoveField(
            model_name='item',
            name='workflow_category',
        ),
        migrations.RemoveField(
            model_name='teamperson',
            name='person',
        ),
        migrations.RemoveField(
            model_name='teamperson',
            name='team',
        ),
        migrations.RemoveField(
            model_name='workflow',
            name='leaders',
        ),
        migrations.RemoveField(
            model_name='workflow',
            name='teams',
        ),
        migrations.RemoveField(
            model_name='workflowcategory',
            name='workflow',
        ),
        migrations.RemoveField(
            model_name='workflowinstanceitems',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='workflowinstanceitems',
            name='item',
        ),
        migrations.RemoveField(
            model_name='workflowinstanceitems',
            name='validation',
        ),
        migrations.RemoveField(
            model_name='workflowinstanceitems',
            name='workflowinstance',
        ),
        migrations.RemoveField(
            model_name='person',
            name='django_user',
        ),
        migrations.RemoveField(
            model_name='person',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='person',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='workflowinstance',
            name='workflow',
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='members', to='workflow.Person'),
        ),
        migrations.AlterField(
            model_name='contracttype',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(related_name='leader', to='workflow.Person'),
        ),
        migrations.AlterField(
            model_name='workflowinstance',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.DeleteModel(
            name='CommentInstanceItem',
        ),
        migrations.DeleteModel(
            name='Competence',
        ),
        migrations.DeleteModel(
            name='CompetencesSubject',
        ),
        migrations.DeleteModel(
            name='CompetencesSubjectCategory',
        ),
        migrations.DeleteModel(
            name='CompetencesType',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='TeamPerson',
        ),
        migrations.DeleteModel(
            name='Validation',
        ),
        migrations.DeleteModel(
            name='Workflow',
        ),
        migrations.DeleteModel(
            name='WorkflowCategory',
        ),
        migrations.DeleteModel(
            name='WorkflowInstanceItems',
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ForeignKey(to='workflow.Team'),
        ),
        migrations.AddField(
            model_name='iteminstance',
            name='assigned_to',
            field=models.ForeignKey(blank=True, to='workflow.Person', null=True),
        ),
        migrations.AddField(
            model_name='iteminstance',
            name='item_model',
            field=models.ForeignKey(to='workflow.ItemModel'),
        ),
        migrations.AddField(
            model_name='iteminstance',
            name='workflow',
            field=models.ForeignKey(to='workflow.WorkflowInstance'),
        ),
        migrations.AddField(
            model_name='competenceinstance',
            name='person',
            field=models.ForeignKey(to='workflow.Person'),
        ),
        migrations.AddField(
            model_name='competenceinstance',
            name='techno',
            field=models.ForeignKey(to='workflow.CompetenceSubject'),
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(to='workflow.ItemInstance'),
        ),
        migrations.AddField(
            model_name='comment',
            name='person',
            field=models.ForeignKey(to='workflow.Person'),
        ),
        migrations.AddField(
            model_name='workflowinstance',
            name='project',
            field=models.ForeignKey(to='workflow.Project'),
        ),
    ]
