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
from workflow.apps.team.models import Person, Team, ContractType, CompetenceCategory, CompetenceSubject
from workflow.apps.workflow.models import Project, WorkflowInstance, ItemCategory, ItemModel

contract = ContractType.objects.all()[0]
superuser = Person.objects.all()[0]

# person + team

PERSON_PER_TEAM = 5
TEAM_NAMES = ('tech', 'com', 'stagiaires')
for team_id in range(3):
    for person_id in range(PERSON_PER_TEAM):
        pseudo = 'user %d' % (team_id*PERSON_PER_TEAM+person_id)
        u = User.objects.create_user(pseudo, 'some@mail.fr', 'pass')
        u.save()
        p = Person.objects.create(user=u, arrival_date=now(), contract_type=contract)

    dreamteam = Team.objects.create(name=TEAM_NAMES[team_id], leader=superuser)
    dreamteam.members = Person.objects.all()[team_id*PERSON_PER_TEAM:(team_id+1)*PERSON_PER_TEAM]
    dreamteam.save()

# competence

COMP = {
    'VCS': ['Git', 'SVN', 'Mercurial', 'Dropbox'],
    'Front': ['HTML/CSS', 'JS', 'Backbones'],
    'Back': ['Python', 'Django', 'Couch', 'Elastic'],
}

for comp_cat, comps in COMP.items():
    cat = CompetenceCategory.objects.create(name=comp_cat)

    for comp in comps:
        c = CompetenceSubject.objects.create(name=comp, category=cat, description='')

# todo comptences instances

# items

ITEMS = {
    'Front': ['Compiler / minifier les fichiers statiques', 'Checker l\'auth', 'Creer une page'],
    'Back': ['Checker la recherche'],
    'Backoffice': ['Verifier la page 1', 'Verifier la page 2', 'Verifier la page 3'],
    'Deployement': ['Backups', 'Copie des nouveaux fichiers de conf', 'Redemarrer les workers'],
}

for cat, items in ITEMS.items():
    cat = ItemCategory.objects.create(name=cat)

    for item in items:
        i = ItemModel.objects.create(name=item, category=cat, description='')

# projects

p = Project.objects.create(name='Findspire', team=dreamteam)
p.items = ItemModel.objects.all()
p.save()
w = WorkflowInstance.objects.create(project=p, version='0.42')

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
