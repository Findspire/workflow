#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from django.core.urlresolvers import reverse
from django.test import TestCase

from workflow.apps.team.models import Person, Team, SkillCategory, SkillSubject, Skill


class MiscTest(TestCase):
    fixtures = ['auth_user']

    def test_index_not_logged(self):
        resp = self.client.get(reverse('team:index'))
        self.assertEqual(resp.status_code, 302)

    def test_index_logged(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

        resp = self.client.get(reverse('team:index'))
        self.assertEqual(resp.status_code, 200)


class PersonTest(TestCase):
    fixtures = ['auth_user', 'team_all']

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
            'skills': [1, 2, 3],
        }
        resp = self.client.post(reverse('team:person_new'), data)
        self.assertEqual(resp.status_code, 302)

        person_count = Person.objects.filter(user__username='Mick').count()
        self.assertEqual(person_count, 1)

        person = Person.objects.get(user__username='Mick')
        comp_list = [c.pk for c in Skill.objects.filter(person=person)]
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
            'skills': [1, 2, 4],
        }
        resp = self.client.post(reverse('team:person_edit', args=[person_pk]), data)
        self.assertEqual(resp.status_code, 302)

        person_count = Person.objects.filter(user__first_name='Mickael').count()
        self.assertEqual(person_count, 0)
        person_count = Person.objects.filter(user__first_name='Anon').count()
        self.assertEqual(person_count, 1)

        person = Person.objects.get(user__username='Mick')
        comp_list = [c.pk for c in Skill.objects.filter(person=person)]
        self.assertEqual(comp_list, [1, 2, 4])

    def test_person_list(self):
        resp = self.client.get(reverse('team:person_list'))
        self.assertEqual(resp.status_code, 200)
        has_person = Person.objects.get(user__username='user 0') in resp.context[-1]['object_list']
        self.assertEqual(has_person, True)

    def test_person_form_errors(self):
        data = {
            'username': '',
            'first_name': 'Mickael',
            'last_name': 'Bay',
            'arrival_date': '2015-01-01',
            'contract_type': 1,
            'skills': [1, 2, 3],
        }
        resp = self.client.post(reverse('team:person_new'), data)
        self.assertEqual(resp.status_code, 200)

        data = {
            'username': 'Mick',
            'first_name': 'Mickael',
            'last_name': 'Bay',
            'arrival_date': '',
            'contract_type': 1,
            'skills': [1, 2, 3],
        }
        resp = self.client.post(reverse('team:person_new'), data)
        self.assertEqual(resp.status_code, 200)


class TeamTest(TestCase):
    fixtures = ['auth_user', 'team_all']

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

        team_count = Team.objects.filter(name='DreamTeam').count()
        self.assertEqual(team_count, 0)
        team_count = Team.objects.filter(name='XV de france').count()
        self.assertEqual(team_count, 1)

    def test_team_list(self):
        resp = self.client.get(reverse('team:team_list'))
        self.assertEqual(resp.status_code, 200)
        has_team = Team.objects.get(name='tech') in resp.context[-1]['object_list']
        self.assertEqual(has_team, True)


class SkillsCategoryTest(TestCase):
    fixtures = ['auth_user', 'team_all']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_skill_category(self):
        # create

        resp = self.client.get(reverse('team:skill_category_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'Tests',
        }
        resp = self.client.post(reverse('team:skill_category_new'), data)
        self.assertEqual(resp.status_code, 302)

        comp_count = SkillCategory.objects.filter(name='Tests').count()
        self.assertEqual(comp_count, 1)

        # update

        comp_pk = SkillCategory.objects.get(name='Tests').pk

        resp = self.client.get(reverse('team:skill_category_edit', args=[comp_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'Front-end',
        }
        resp = self.client.post(reverse('team:skill_category_edit', args=[comp_pk]), data)
        self.assertEqual(resp.status_code, 302)

        comp_count = SkillCategory.objects.filter(name='Tests').count()
        self.assertEqual(comp_count, 0)
        comp_count = SkillCategory.objects.filter(name='Front-end').count()
        self.assertEqual(comp_count, 1)


class SkillsSubjectTest(TestCase):
    fixtures = ['auth_user', 'team_all']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_skill_subject(self):
        # create

        resp = self.client.get(reverse('team:skill_subject_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'Some skills',
            'category': SkillCategory.objects.get(name='Front').pk,
            'description': 'Some description',
        }
        resp = self.client.post(reverse('team:skill_subject_new'), data)
        self.assertEqual(resp.status_code, 302)

        comp_count = SkillSubject.objects.filter(name='Some skills').count()
        self.assertEqual(comp_count, 1)

        # update

        comp_pk = SkillSubject.objects.get(name='Some skills').pk

        resp = self.client.get(reverse('team:skill_subject_edit', args=[comp_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'Some other skills',
            'category': SkillCategory.objects.get(name='Front').pk,
            'description': 'Some description',
        }
        resp = self.client.post(reverse('team:skill_subject_edit', args=[comp_pk]), data)
        self.assertEqual(resp.status_code, 302)

        comp_count = SkillSubject.objects.filter(name='Some skills').count()
        self.assertEqual(comp_count, 0)
        comp_count = SkillSubject.objects.filter(name='Some other skills').count()
        self.assertEqual(comp_count, 1)

    def test_skill_subject_list(self):
        resp = self.client.get(reverse('team:skill_subject_list'))
        self.assertEqual(resp.status_code, 200)
        comp = SkillSubject.objects.get(name='HTML')
        # the following line is tricky, see the corresponding view to understand
        has_comp = any(comp in comp_list for comp_list in resp.context[-1]['categories'].values())
        self.assertEqual(has_comp, True)


class SkillsInstancesTest(TestCase):
    fixtures = ['auth_user', 'team_all']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_skill_instance(self):
        # create

        """
        todo : make me pass and test the ajax calls

        resp = self.client.get(reverse('team:skill_instance_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'techno': SkillSubject.objects.get(pk=1).pk,
            'person': Person.objects.get(pk=1).pk,
            'strength': 1,
        }
        resp = self.client.post(reverse('team:skill_instance_new'), data)
        self.assertEqual(resp.status_code, 302)

        comp_count = Skill.objects.filter(techno__pk=1, person__pk=1).count()
        self.assertEqual(comp_count, 1)

        # update

        person_pk = Person.objects.get(pk=1).pk
        resp = self.client.get(reverse('team:skill_instance_list', args=[person_pk]))

        some_object_pk = resp.context['myformset'].forms[0].instance.pk

        # management form, used internally by django.
        data = {'form-'+key: value for key, value in resp.context['myformset'].management_form.initial.items()}

        data.update({
            'form-0-id': some_object_pk,
            'form-0-strength': 42,
        })

        resp = self.client.post(reverse('team:skill_instance_list', args=[person_pk]), data)
        self.assertEqual(resp.status_code, 302)

        skill = Skill.objects.get(pk=some_object_pk)
        self.assertEqual(skill.strength, 42)

        """
