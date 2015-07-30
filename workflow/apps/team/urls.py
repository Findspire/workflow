#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('workflow.apps.team',
    url(r'^$', 'views.index', name='index'),

    url(r'^person/new/$', views.person_handle_form, name='person_new'),
    url(r'^person/edit/(?P<pk>\d+)/$', views.person_handle_form, name='person_edit'),
    url(r'^person/list/$', views.person_list, name='person_list'),

    url(r'^competence/new/$', views.CompetenceInstanceView.as_view(), name='competence_instance_new'),
    url(r'^competence/edit/(?P<pk>\d+)/$', views.CompetenceInstanceView.as_view(), name='competence_instance_edit'),

    url(r'^competence/subject/new/$', views.CompetenceSubjectView.as_view(), name='competence_subject_new'),
    url(r'^competence/subject/new/(?P<category>\d+)/$', views.CompetenceSubjectView.as_view(), name='competence_subject_new'),
    url(r'^competence/subject/edit/(?P<pk>\d+)/$', views.CompetenceSubjectView.as_view(), name='competence_subject_edit'),
    url(r'^competence/subject/list/$', views.competence_subject_list, name='competence_subject_list'),

    url(r'^competence/category/new/$', views.CompetenceCategoryView.as_view(), name='competence_category_new'),
    url(r'^competence/category/edit/(?P<pk>\d+)/$', views.CompetenceCategoryView.as_view(), name='competence_category_edit'),

    url(r'^team/new/$', views.TeamView.as_view(), name='team_new'),
    url(r'^team/edit/(?P<pk>\d+)/$', views.TeamView.as_view(), name='team_edit'),
    url(r'^team/list/$', views.team_list, name='team_list'),
)
