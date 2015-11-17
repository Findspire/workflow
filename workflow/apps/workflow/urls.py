#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire

from django.conf.urls import patterns, url
from workflow.apps.workflow import views


urlpatterns = patterns('workflow.apps.workflow',
    url(r'^$', 'views.index', name='index'),

    url(r'^project/new/$', views.ProjectFormView.as_view(), name='project_new'),
    url(r'^project/edit/(?P<pk>\d+)/$', views.ProjectFormView.as_view(), name='project_edit'),
    url(r'^project/list/$', views.project_list, name='project_list'),

    url(r'^workflow/new/$', views.WorkflowFormView.as_view(), name='workflow_new'),
    url(r'^workflow/new/(?P<project>\d+)/$', views.WorkflowFormView.as_view(), name='workflow_new'),
    url(r'^workflow/edit/(?P<pk>\d+)/$', views.WorkflowFormView.as_view(), name='workflow_edit'),
    url(r'^workflow/show/(?P<workflow_pk>\d+)/(?P<which_display>\w+)/$', views.workflow_show, name='workflow_show'),
    url(r'^workflow/(?P<workflow_pk>\d+)/delete/$', views.workflow_delete, name='workflow_delete'),

    url(r'^item/model/new/$', views.ItemModelFormView.as_view(), name='item_model_new'),
    url(r'^item/model/new/category/(?P<category>\d+)$', views.ItemModelFormView.as_view(), name='item_model_new'),
    url(r'^item/model/new/workflow/(?P<workflow_pk>\d+)$', views.ItemModelFormViewFromWorkflow.as_view(), name='item_model_add_to_workflow'),
    url(r'^item/model/new/workcat/(?P<workflow_pk>\d+)/(?P<category>\d+)$', views.create_item_view, name='item_model_add_to_workcat'),
    url(r'^item/model/edit/(?P<pk>\d+)/$', views.ItemModelFormView.as_view(), name='item_model_edit'),
    url(r'^item/model/list/$', views.itemmodel_list, name='item_model_list'),

    url(r'^item/category/new/$', views.ItemCategoryFormView.as_view(), name='item_category_new'),
    url(r'^item/category/new/(?P<workflow_pk>\d+)/$', views.ItemCategoryFormView.as_view(), name='item_category_new'),
    url(r'^item/category/edit/(?P<pk>\d+)/$', views.ItemCategoryFormView.as_view(), name='item_category_edit'),

    url(r'^item/instance/show/(?P<item_pk>\d+)/$', views.item_instance_show, name='item_instance_show'),
    url(r'^item/instance/delete/(?P<workflow_pk>\d+)/(?P<item_pk>\d+)/$', views.delete_item_view, name='delete_item_view'),
    url(r'^item/instance/comment/(?P<workflow_pk>\d+)/(?P<comment_pk>\d+)/delete/$', views.delete_comment_view, name='delete_comment_view'),
    url(r'^item/instance/get-comments/(?P<item_pk>\d+)/$', views.get_comments, name='get_item_comments'),
    url(r'^update/(?P<which_display>\w+)/(?P<action>\w+)/(?P<model>\w+)/(?P<pk>\d+)/$', views.update, name='update'),
    url(r'^update/(?P<which_display>\w+)/(?P<action>\w+)/(?P<model>\w+)/(?P<pk>\d+)/(?P<pk_other>\d+)/$', views.update, name='update'),
    url(r'^update/(?P<action>\w+)/(?P<item_pk>\d+)/', views.update_item_validation, name='update_item_validation'),
    url(r'^drag-item/(?P<item_pk>[0-9]+)(?:/(?P<related_pk>[0-9]+))?/$', views.drag_item, name='drag_item'),
)
