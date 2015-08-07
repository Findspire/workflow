#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workflow.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils.timezone import now
from workflow.apps.team.models import Person

# clean
print '=> Cleaning everything ...'
os.system('rm workflow.db')
print '=> Done'

# build db
print '=> Migrate db'
os.system('python manage.py migrate')
print '=> Done'

# create super user
print '=> Creating super user ...'

u = User.objects.create_superuser('admin', 'admin@admin.fr', 'admin')
u.save()
p = Person.objects.create(user=u, arrival_date=now())

# todo create a Group "manager" and add yourself

print '=> Done'
