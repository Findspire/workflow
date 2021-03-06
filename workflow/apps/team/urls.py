#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire

from django.conf.urls import patterns, url
from workflow.apps.team import views


urlpatterns = patterns('workflow.apps.team',
    url(r'^$', 'views.index', name='index'),

    url(r'^person/new/$', views.person_handle_form, name='person_new'),
    url(r'^person/edit/(?P<person_pk>\d+)/$', views.person_handle_form, name='person_edit'),
    url(r'^person/list/$', views.PersonListView.as_view(), name='person_list'),

    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),

    url(r'^skill/list/(?P<person_pk>\d+)/$', views.skills_list, name='skill_instance_list'),

    url(r'^skill/subject/new/$', views.SkillSubjectView.as_view(), name='skill_subject_new'),
    url(r'^skill/subject/new/(?P<category>\d+)/$', views.SkillSubjectView.as_view(), name='skill_subject_new'),
    url(r'^skill/subject/edit/(?P<pk>\d+)/$', views.SkillSubjectView.as_view(), name='skill_subject_edit'),
    url(r'^skill/subject/list/$', views.skill_subject_list, name='skill_subject_list'),

    url(r'^skill/category/new/$', views.SkillCategoryView.as_view(), name='skill_category_new'),
    url(r'^skill/category/edit/(?P<pk>\d+)/$', views.SkillCategoryView.as_view(), name='skill_category_edit'),

    url(r'^team/new/$', views.TeamView.as_view(), name='team_new'),
    url(r'^team/edit/(?P<pk>\d+)/$', views.TeamView.as_view(), name='team_edit'),
    url(r'^team/list/$', views.TeamListView.as_view(), name='team_list'),
)
