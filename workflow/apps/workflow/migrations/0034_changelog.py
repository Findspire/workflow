# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0033_auto_20160112_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Changelog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='Title', max_length=50)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Changelog',
                'verbose_name_plural': 'Changelog',
            },
        ),
    ]
