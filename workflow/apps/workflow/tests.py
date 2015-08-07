#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from django.core.urlresolvers import reverse
from django.test import TestCase

from workflow.apps.workflow.models import Project, Workflow, ItemCategory, ItemModel, Item


class MiscTest(TestCase):
    fixtures = ['auth_user']

    def test_index_not_logged(self):
        resp = self.client.get(reverse('workflow:index'))
        self.assertEqual(resp.status_code, 302)

    def test_index_logged(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

        resp = self.client.get(reverse('workflow:index'))
        self.assertEqual(resp.status_code, 200)


class ProjectTest(TestCase):
    fixtures = ['auth_user', 'team_all', 'workflow']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_project_create(self):
        resp = self.client.get(reverse('workflow:project_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'new project',
            'team': 1,
            'items': [1, 2, 3, 5],
        }
        resp = self.client.post(reverse('workflow:project_new'), data)
        self.assertEqual(resp.status_code, 302)

        project_count = Project.objects.filter(name='new project').count()
        self.assertEqual(project_count, 1)
        project_items = [item.pk for item in Project.objects.get(name='new project').items.all()]
        self.assertEqual(project_items, [1, 2, 3, 5])

    def test_project_edit(self):
        project_pk = Project.objects.get(name='project 1').pk

        resp = self.client.get(reverse('workflow:project_edit', args=[project_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'project 1 edited',
            'team': 1,
            'items': [1, 2, 3, 6],
        }
        resp = self.client.post(reverse('workflow:project_edit', args=[project_pk]), data)
        self.assertEqual(resp.status_code, 302)

        project_count = Project.objects.filter(name='project 1').count()
        self.assertEqual(project_count, 0)
        project_count = Project.objects.filter(name='project 1 edited').count()
        self.assertEqual(project_count, 1)
        project_items = [item.pk for item in Project.objects.get(name='project 1 edited').items.all()]
        self.assertEqual(project_items, [1, 2, 3, 6])

    def test_project_list(self):
        resp = self.client.get(reverse('workflow:project_list'))
        self.assertEqual(resp.status_code, 200)
        project = Project.objects.get(name='project 1')
        has_project = project in resp.context[-1]['projects'].keys()
        self.assertEqual(has_project, True)


class WorkflowTest(TestCase):
    fixtures = ['auth_user', 'team_all', 'workflow']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_workflow_create(self):
        resp = self.client.get(reverse('workflow:workflow_new'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('workflow:workflow_new', args=[1]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'project': 1,
            'version': 'new workflow',
        }
        resp = self.client.post(reverse('workflow:workflow_new'), data)
        self.assertEqual(resp.status_code, 302)

        workflow_count = Workflow.objects.filter(project__pk=1, version='new workflow').count()
        self.assertEqual(workflow_count, 1)

        project_items = [item.pk for item in Project.objects.get(pk=1).items.all()]
        workflow = Workflow.objects.get(project__pk=1, version='new workflow')
        workflow_items = [item.item_model.pk for item in Item.objects.filter(workflow=workflow)]
        self.assertEqual(project_items, workflow_items)

    def test_workflow_edit(self):
        workflow_pk = Workflow.objects.get(project__pk=1, version='workflow 1').pk

        resp = self.client.get(reverse('workflow:workflow_edit', args=[workflow_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'project': 1,
            'version': 'workflow 1 edited',
        }
        resp = self.client.post(reverse('workflow:workflow_edit', args=[workflow_pk]), data)
        self.assertEqual(resp.status_code, 302)

        workflow_count = Workflow.objects.filter(project__pk=1, version='workflow 1').count()
        self.assertEqual(workflow_count, 0)
        workflow_count = Workflow.objects.filter(project__pk=1, version='workflow 1 edited').count()
        self.assertEqual(workflow_count, 1)

    def test_workflow_list(self):
        resp = self.client.get(reverse('workflow:project_list'))
        self.assertEqual(resp.status_code, 200)
        workflow = Workflow.objects.get(project__pk=1, version='workflow 1')
        has_workflow = any([workflow in workflow_list for workflow_list in resp.context[-1]['projects'].values()])
        self.assertEqual(has_workflow, True)

    def test_workflow_show(self):
        workflow_pk = Workflow.objects.get(project__pk=1, version='workflow 1').pk

        resp = self.client.get(reverse('workflow:workflow_show', args=[workflow_pk, 'thisShouldRaiseA404']))
        self.assertEqual(resp.status_code, 404)

        for which_display in ('all', 'mine', 'untested', 'success', 'failed', 'untaken'):#, 'taken'):
            resp = self.client.get(reverse('workflow:workflow_show', args=[workflow_pk, which_display]))
            self.assertEqual(resp.status_code, 200)

            itemmodel = ItemModel.objects.get(name='item model '+which_display)
            item = Item.objects.get(item_model=itemmodel)
            has_item = any([item in item_list for item_list in resp.context[-1]['items'].values()])
            self.assertEqual(has_item, True)

    def test_item_show(self):
        resp = self.client.get(reverse('workflow:item_instance_show', args=[1]))
        self.assertEqual(resp.status_code, 200)

        # description
        item = Item.objects.get(pk=1)
        itemmodel = Item.objects.get(pk=1).item_model

        self.assertEqual(itemmodel.description, '')

        data = {
            'type': 'description',
            'description': 'Some new description',
        }
        resp = self.client.post(reverse('workflow:item_instance_show', args=[item.pk]), data)
        self.assertEqual(resp.status_code, 302)

        itemmodel = Item.objects.get(pk=1).item_model
        self.assertEqual(itemmodel.description, 'Some new description')

        # comment

        # todo


    def test_item_update(self):
        pass
        """
            url(r'^update/(?P<action>\w+)/(?P<model>\w+)/(?P<pk>\d+)/$'
                name='update'),
            url(r'^update/(?P<action>\w+)/(?P<model>\w+)/(?P<pk>\d+)/(?P<pk_other>\d+)/$'
                name='update'),
        """


class ItemModelTest(TestCase):
    fixtures = ['auth_user', 'team_all', 'workflow']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_item_model_create(self):
        resp = self.client.get(reverse('workflow:item_model_new'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('workflow:item_model_new', args=[1]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'new item model',
            'category': 1,
            'description': 'Some description',
        }
        resp = self.client.post(reverse('workflow:item_model_new'), data)
        self.assertEqual(resp.status_code, 302)

        person_count = ItemModel.objects.filter(name='new item model').count()
        self.assertEqual(person_count, 1)

    def test_item_model_edit(self):
        item_pk = ItemModel.objects.get(name='item model 1').pk

        resp = self.client.get(reverse('workflow:item_model_edit', args=[item_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'item model 1 edited',
            'category': 1,
            'description': 'Some description',
        }
        resp = self.client.post(reverse('workflow:item_model_edit', args=[item_pk]), data)
        self.assertEqual(resp.status_code, 302)

        item_count = ItemModel.objects.filter(name='item model 1').count()
        self.assertEqual(item_count, 0)
        item_count = ItemModel.objects.filter(name='item model 1 edited').count()
        self.assertEqual(item_count, 1)

    def test_item_model_list(self):
        resp = self.client.get(reverse('workflow:item_model_list'))
        self.assertEqual(resp.status_code, 200)
        item = ItemModel.objects.get(name='item model 1')
        has_item = any(item in item_list for item_list in resp.context[-1]['categories'].values())
        self.assertEqual(has_item, True)


class ItemCategoryTest(TestCase):
    fixtures = ['auth_user', 'team_all', 'workflow']

    def setUp(self):
        resp = self.client.login(username='admin', password='admin')
        self.assertEqual(resp, True)

    def test_item_category_create(self):
        resp = self.client.get(reverse('workflow:item_category_new'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'item category new',
        }
        resp = self.client.post(reverse('workflow:item_category_new'), data)
        self.assertEqual(resp.status_code, 302)

        items_count = ItemCategory.objects.filter(name='item category new').count()
        self.assertEqual(items_count, 1)

    def test_item_category_edit(self):
        item_pk = ItemCategory.objects.get(name='item category 1').pk

        resp = self.client.get(reverse('workflow:item_category_edit', args=[item_pk]))
        self.assertEqual(resp.status_code, 200)

        data = {
            'name': 'item category 1 edited',
        }
        resp = self.client.post(reverse('workflow:item_category_edit', args=[item_pk]), data)
        self.assertEqual(resp.status_code, 302)

        item_count = ItemCategory.objects.filter(name='item category 1').count()
        self.assertEqual(item_count, 0)
        item_count = ItemCategory.objects.filter(name='item category 1 edited').count()
        self.assertEqual(item_count, 1)
