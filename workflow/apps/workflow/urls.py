#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('workflow.apps.workflow',
    url(r'^$', 'views.index', name='index'),

    url(r'^project/new/$', views.ProjectFormView.as_view(), name='project_new'),
    url(r'^project/edit/(?P<pk>\d+)/$', views.ProjectFormView.as_view(), name='project_edit'),
    url(r'^project/list/$', views.project_list, name='project_list'),

    url(r'^workflow/new/$', views.WorkflowFormView.as_view(), name='workflow_new'),
    url(r'^workflow/new/(?P<project>\d+)/$', views.WorkflowFormView.as_view(), name='workflow_new'),
    url(r'^workflow/edit/(?P<pk>\d+)/$', views.WorkflowFormView.as_view(), name='workflow_edit'),
    url(r'^workflow/show/(?P<workflow_pk>\d+)/(?P<which_display>\w+)/$', views.workflow_show, name='workflow_show'),

    url(r'^item/model/new/$', views.ItemModelFormView.as_view(), name='item_model_new'),
    url(r'^item/model/new/(?P<category>\d+)$', views.ItemModelFormView.as_view(), name='item_model_new'),
    url(r'^item/model/edit/(?P<pk>\d+)/$', views.ItemModelFormView.as_view(), name='item_model_edit'),
    url(r'^item/model/list/$', views.item_model_list, name='item_model_list'),

    url(r'^item/category/new/$', views.ItemCategoryFormView.as_view(), name='item_category_new'),
    url(r'^item/category/edit/(?P<pk>\d+)/$', views.ItemCategoryFormView.as_view(), name='item_category_edit'),

    url(r'^item/instance/show/(?P<item_pk>\d+)/$', views.item_instance_show, name='item_instance_show'),
    url(r'^update/(?P<action>\w+)/(?P<model>\w+)/(?P<pk>\d+)/$', views.update, name='update'),
    url(r'^update/(?P<action>\w+)/(?P<model>\w+)/(?P<pk>\d+)/(?P<pk_other>\d+)/$', views.update, name='update'),
)
