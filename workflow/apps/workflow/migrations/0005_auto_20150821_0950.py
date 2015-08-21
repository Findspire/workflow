# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0004_rename_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(verbose_name='Item', to='workflow.Item'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='person',
            field=models.ForeignKey(verbose_name='Person', to='team.Person'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=1000, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='item',
            name='assigned_to',
            field=models.ForeignKey(verbose_name='Assigned to', blank=True, to='team.Person', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_model',
            field=models.ForeignKey(verbose_name='Item model', to='workflow.ItemModel'),
        ),
        migrations.AlterField(
            model_name='item',
            name='validation',
            field=models.SmallIntegerField(default=0, verbose_name='Validation', choices=[(0, 'Untested'), (1, 'Success'), (2, 'Failed')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='workflow',
            field=models.ForeignKey(verbose_name='Workflow', to='workflow.Workflow'),
        ),
        migrations.AlterField(
            model_name='itemcategory',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='category',
            field=models.ForeignKey(verbose_name='Category', to='workflow.ItemCategory'),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='description',
            field=models.TextField(max_length=1000, null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='items',
            field=models.ManyToManyField(to='workflow.ItemModel', verbose_name='Items', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='team.Team'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='creation_date',
            field=models.DateField(auto_now=True, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='project',
            field=models.ForeignKey(verbose_name='Project', to='workflow.Project'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='version',
            field=models.CharField(max_length=128, verbose_name='Version'),
        ),
    ]
