#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('workflow.apps.team',
    url(r'^$', 'views.index', name='index'),

    url(r'^competence/new/$', views.CompetenceInstanceView.as_view(), name='competence_new'),
    url(r'^competence/edit/(?P<pk>\d+)/$', views.CompetenceInstanceView.as_view(), name='competence_edit'),
    url(r'^competence/list/$', views.CompetenceInstanceListView.as_view(), name='competence_list'),

    url(r'^competence/subject/new/$', views.CompetenceSubjectView.as_view(), name='competence_subject_new'),
    url(r'^competence/subject/edit/(?P<pk>\d+)/$', views.CompetenceSubjectView.as_view(), name='competence_subject_edit'),
    url(r'^competence/subject/list/$', views.CompetenceSubjectListView.as_view(), name='competence_subject_list'),

    url(r'^competence/category/new/$', views.CompetenceCategoryView.as_view(), name='competence_category_new'),
    url(r'^competence/category/edit/(?P<pk>\d+)/$', views.CompetenceCategoryView.as_view(), name='competence_category_edit'),
    url(r'^competence/category/list/$', views.CompetenceCategoryListView.as_view(), name='competence_category_list'),
)

#Person
#Team
