#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workflow.settings")
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now
from workflow.apps.team.models import Person, Team, ContractType, CompetenceCategory, CompetenceSubject
from workflow.apps.workflow.models import Project, WorkflowInstance, ItemCategory, ItemModel

contract = ContractType.objects.all()[0]
superuser = Person.objects.all()[0]

# person + team
for i in range(10):
    pseudo = 'user %d' % i
    u = User.objects.create_user(pseudo, 'some@mail.fr', 'pass')
    u.save()
    p = Person(user=u, arrival_date=now(), contract_type=contract)
    p.save()

dreamteam = Team(name='dev', leader=superuser)
dreamteam.save()
dreamteam.members = Person.objects.all()
dreamteam.save()

# competence

COMP = {
    'VCS': ['Git', 'SVN', 'Mercurial', 'Dropbox'],
    'Front': ['HTML/CSS', 'JS', 'Backbones'],
    'Back': ['Python', 'Django', 'Couch', 'Elastic'],
}

for comp_cat, comps in COMP.items():
    cat = CompetenceCategory(name=comp_cat)
    cat.save()

    for comp in comps:
        c = CompetenceSubject(name=comp, category=cat, description='')
        c.save()

# items

ITEMS = {
    'Front': ['Compiler / minifier les fichiers statiques', 'Checker l\'auth', 'Creer une page'],
    'Back': ['Checker la recherche'],
    'Backoffice': ['Verifier la page 1', 'Verifier la page 2', 'Verifier la page 3'],
    'Deployement': ['Backups', 'Copie des nouveaux fichiers de conf', 'Redemarrer les workers'],
}

for cat, items in ITEMS.items():
    cat = ItemCategory(name=cat)
    cat.save()

    for item in items:
        i = ItemModel(name=item, category=cat, description='')
        i.save()

# projects
p = Project(name='Findspire', team=dreamteam)
p.save()
p.items = ItemModel.objects.all()
p.save()
w = WorkflowInstance(project=p, version='0.42')
w.save()

"""
randomize ItemInstance
    assigned_to
    validation

random Comment
    item = models.ForeignKey(ItemInstance)
    person = models.ForeignKey(Person)
    date = models.DateField(default=timezone.now)
    text = models.TextField(max_length=1000)
"""
