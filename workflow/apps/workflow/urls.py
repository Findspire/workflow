#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('workflow.apps.workflow',
    url(r'^new/$',                                                              'views.workflowinstance_new',               name='workflow-workflowinstance-new'),
    url(r'^list/$',                                                             'views.workflowinstance_list',              name='workflow-workflowinstance-list'),
    url(r'^show/(?P<workflowinstance_id>\d+)/(?P<which_display>\w+)/$',         'views.workflowinstance_show',              name='workflow-workflowinstance-show'),
    url(r'^delete/(?P<workflowinstance_id>\d+)/$',                              'views.workflowinstance_delete',            name='workflow-workflowinstance-delete'),
    url(r'^category/take/(?P<workflowinstance_id>\d+)/(?P<category_id>\d+)/$',  'views.workflowinstance_take_category',     name='workflow-workflowinstance-take_category'),
    url(r'^category/untake/(?P<workflowinstance_id>\d+)/(?P<category_id>\d+)/$', 'views.workflowinstance_untake_category',  name='workflow-workflowinstance-untake_category'),
    url(r'^item/take/(?P<workflowinstanceitem_id>\d+)/$',                       'views.workflowinstanceitem_take',          name='workflow-workflowinstanceitem-take'),
    url(r'^item/untake/(?P<workflowinstanceitem_id>\d+)/$',                     'views.workflowinstanceitem_untake',        name='workflow-workflowinstanceitem-untake'),
    url(r'^item/validate/(?P<workflowinstanceitem_id>\d+)/(?P<validation_label>\w+)/$', 'views.workflowinstanceitem_validate', name='workflow-workflowinstanceitem-validate'),
    url(r'^item/no_state/(?P<workflowinstanceitem_id>\d+)/$',                   'views.workflowinstanceitem_no_state',      name='workflow-workflowinstanceitem-nostate'),
    url(r'^item/show/(?P<workflowinstanceitem_id>\d+)/$',                       'views.workflowinstanceitem_show',          name='workflow-workflowinstanceitem-show'),
    url(r'^check/(?P<item_id>\d+)/(?P<category_id>\d+)/$',                      'views.check_state_before_change',          name='workflow-check-state'),
)
