#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('workflow.apps.team',
    url(r'^$', 'views.index', name='index'),

    url(r'^competence/new/$', views.CompetenceInstanceView.as_view(), name='competence_new'),
    url(r'^competence/edit/(?P<pk>\d+)/$', views.CompetenceInstanceView.as_view(), name='competence_edit'),
    url(r'^competence/list/$', views.competences_list, name='competences_list'),

    url(r'^competence/subject/new/$', views.CompetenceSubjectView.as_view(), name='competence_subject_new'),
    url(r'^competence/subject/new/(?P<category>\d+)/$', views.CompetenceSubjectView.as_view(), name='competence_subject_new'),
    url(r'^competence/subject/edit/(?P<pk>\d+)/$', views.CompetenceSubjectView.as_view(), name='competence_subject_edit'),

    url(r'^competence/category/new/$', views.CompetenceCategoryView.as_view(), name='competence_category_new'),
    url(r'^competence/category/edit/(?P<pk>\d+)/$', views.CompetenceCategoryView.as_view(), name='competence_category_edit'),

    url(r'^team/new/$', views.TeamView.as_view(), name='team_new'),
    url(r'^team/edit/(?P<pk>\d+)/$', views.TeamView.as_view(), name='team_edit'),
    url(r'^team/list/$', views.team_list, name='team_list'),
)
