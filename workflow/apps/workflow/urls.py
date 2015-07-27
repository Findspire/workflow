#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('workflow.apps.workflow',
    url(r'^$', 'views.index', name='index'),
    url(r'^project/new/$', 'views.project_new', name='project_new'),
    url(r'^project/edit/(?P<project_pk>\d+)/$', 'views.project_edit', name='project_edit'),
    url(r'^project/list/$', 'views.project_list', name='project_list'),
    url(r'^workflow/new/$', 'views.workflow_new', name='workflow_new'),
    url(r'^workflow/new/(?P<project_pk>\d+)/$', 'views.workflow_new', name='workflow_new'),
    url(r'^workflow/show/(?P<workflow_pk>\d+)/(?P<which_display>\w+)/$', 'views.workflow_show', name='workflow_show'),
    url(r'^item/model/new/$', 'views.itemmodel_new', name='itemmodel_new'),
    url(r'^item/instance/show/(?P<item_pk>\d+)/$', 'views.iteminstance_show', name='iteminstance_show'),
    url(r'^update/(?P<action>\w+)/(?P<model>\w+)/(?P<pk>\d+)/$', 'views.update', name='update'),
    url(r'^update/(?P<action>\w+)/(?P<model>\w+)/(?P<pk>\d+)/(?P<pk_other>\d+)/$', 'views.update', name='update'),
)
