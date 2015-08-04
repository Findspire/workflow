#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Person, Team, CompetenceCategory, CompetenceSubject, CompetenceInstance


class MiscTest(TestCase):
    fixtures = ['auth_permission', 'auth_user']

    def test_index_not_logged(self):
        resp = self.client.get(reverse('team:index'))
        self.assertEqual(resp.status_code, 302)

    def test_index_logged(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

        resp = self.client.get(reverse('team:index'))
        self.assertEqual(resp.status_code, 200)


class PersonTest(TestCase):
    fixtures = ['auth_permission', 'auth_user', 'team_all']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_person(self):
        # create

        resp = self.client.get(reverse('team:person_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'username': 'Mick',
            'first_name': 'Mickael',
            'last_name': 'Bay',
            'arrival_date': '2015-01-01',
            'contract_type': 1,
            'competences': [1, 2, 3],
        }
        resp = self.client.post(reverse('team:person_new'), data)
        self.assertEqual(resp.status_code, 302)

        person_count = Person.objects.filter(user__username='Mick').count()
        self.assertEqual(person_count, 1)

        person = Person.objects.get(user__username='Mick')
        comp_list = [c.pk for c in CompetenceInstance.objects.filter(person=person)]
        self.assertEqual(comp_list, [1, 2, 3])

        # update

        person_pk = Person.objects.get(user__username='Mick').pk

        resp = self.client.get(reverse('team:person_edit', args=[person_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'username': 'Mick',
            'first_name': 'Anon',
            'last_name': 'imous',
            'arrival_date': '2015-01-01',
            'contract_type': 1,
            'competences': [1, 2, 4],
        }
        resp = self.client.post(reverse('team:person_edit', args=[person_pk]), data)
        self.assertEqual(resp.status_code, 302)

        person_first_name = Person.objects.get(pk=person_pk).user.first_name
        self.assertEqual(person_first_name, 'Anon')

        person = Person.objects.get(user__username='Mick')
        comp_list = [c.pk for c in CompetenceInstance.objects.filter(person=person)]
        self.assertEqual(comp_list, [1, 2, 4])

    def test_person_list(self):
        resp = self.client.get(reverse('team:person_list'))
        self.assertEqual(resp.status_code, 200)
        has_person = Person.objects.get(user__username='user 0') in resp.context[-1]['object_list']
        self.assertEqual(has_person, True)


class TeamTest(TestCase):
    fixtures = ['auth_permission', 'auth_user', 'team_all']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_team(self):
        # create

        resp = self.client.get(reverse('team:team_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'DreamTeam',
            'leader': 1,
            'members': [1, 2, 3, 4, 5],
        }
        resp = self.client.post(reverse('team:team_new'), data)
        self.assertEqual(resp.status_code, 302)

        team_count = Team.objects.filter(name='DreamTeam').count()
        self.assertEqual(team_count, 1)

        # update

        team_pk = Team.objects.get(name='DreamTeam').pk

        resp = self.client.get(reverse('team:team_edit', args=[team_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'XV de france',
            'leader': 1,
            'members': [1, 2, 3, 4, 5],
        }
        resp = self.client.post(reverse('team:team_edit', args=[team_pk]), data)
        self.assertEqual(resp.status_code, 302)

        team_name = Team.objects.get(pk=team_pk).name
        self.assertEqual(team_name, 'XV de france')

    def test_team_list(self):
        resp = self.client.get(reverse('team:team_list'))
        self.assertEqual(resp.status_code, 200)
        has_team = Team.objects.get(name='tech') in resp.context[-1]['object_list']
        self.assertEqual(has_team, True)


class CompetencesCategoryTest(TestCase):
    fixtures = ['auth_permission', 'auth_user', 'team_all']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_competence_category(self):
        # create

        resp = self.client.get(reverse('team:competence_category_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'Tests',
        }
        resp = self.client.post(reverse('team:competence_category_new'), data)
        self.assertEqual(resp.status_code, 302)

        comp_count = CompetenceCategory.objects.filter(name='Tests').count()
        self.assertEqual(comp_count, 1)

        # update

        comp_pk = CompetenceCategory.objects.get(name='Tests').pk

        resp = self.client.get(reverse('team:competence_category_edit', args=[comp_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'Front-end',
        }
        resp = self.client.post(reverse('team:competence_category_edit', args=[comp_pk]), data)
        self.assertEqual(resp.status_code, 302)

        comp_name = CompetenceCategory.objects.get(pk=comp_pk).name
        self.assertEqual(comp_name, 'Front-end')


class CompetencesSubjectTest(TestCase):
    fixtures = ['auth_permission', 'auth_user', 'team_all']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_competence_subject(self):
        # create

        resp = self.client.get(reverse('team:competence_subject_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'Some skill',
            'category': CompetenceCategory.objects.get(name='Front').pk,
            'description': 'Some description',
        }
        resp = self.client.post(reverse('team:competence_subject_new'), data)
        self.assertEqual(resp.status_code, 302)

        comp_count = CompetenceSubject.objects.filter(name='Some skill').count()
        self.assertEqual(comp_count, 1)

        # update

        comp_pk = CompetenceSubject.objects.get(name='Some skill').pk

        resp = self.client.get(reverse('team:competence_subject_edit', args=[comp_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'Some other skill',
            'category': CompetenceCategory.objects.get(name='Front').pk,
            'description': '',
        }
        resp = self.client.post(reverse('team:competence_subject_edit', args=[comp_pk]), data)
        self.assertEqual(resp.status_code, 302)

        comp_name = CompetenceSubject.objects.get(pk=comp_pk).name
        self.assertEqual(comp_name, 'Some other skill')

    def test_competence_subject_list(self):
        resp = self.client.get(reverse('team:competence_subject_list'))
        self.assertEqual(resp.status_code, 200)
        comp = CompetenceSubject.objects.get(name='HTML')
        # the following line is tricky, see the corresponding view to understand
        has_comp = any(comp in comp_list for comp_list in resp.context[-1]['categories'].values())
        self.assertEqual(has_comp, True)


class CompetencesInstancesTest(TestCase):
    fixtures = ['auth_permission', 'auth_user', 'team_all']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_competence_instance(self):
        # create

        resp = self.client.get(reverse('team:competence_instance_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'techno': CompetenceSubject.objects.get(pk=1).pk,
            'person': Person.objects.get(pk=1).pk,
            'strength': 1,
        }
        resp = self.client.post(reverse('team:competence_instance_new'), data)
        self.assertEqual(resp.status_code, 302)

        comp_count = CompetenceInstance.objects.filter(techno__pk=1, person__pk=1).count()
        self.assertEqual(comp_count, 1)

        # update

        comp_pk = CompetenceInstance.objects.get(techno__pk=1, person__pk=1).pk

        resp = self.client.get(reverse('team:competence_instance_edit', args=[comp_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'techno': 1,
            'person': 1,
            'strength': 42,
        }
        resp = self.client.post(reverse('team:competence_instance_edit', args=[comp_pk]), data)
        self.assertEqual(resp.status_code, 302)

        comp_strength = CompetenceInstance.objects.get(pk=comp_pk).strength
        self.assertEqual(comp_strength, 42)

        # list

        resp = self.client.get(reverse('team:competence_instance_list', args=[1]))
        self.assertEqual(resp.status_code, 200)
        comp = CompetenceInstance.objects.get(techno__pk=1, person__pk=1)
        has_comp = comp in resp.context[-1]['object_list']
        self.assertEqual(has_comp, True)
