#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'workflow.apps.workflow.views.index', name='workflowinstance'),
    url(r'^workflow/item/new/$', 'workflow.apps.workflow.views.item_new', name='workflow-item-new'),

    url(r'^workflowinstance/', include('workflow.apps.workflow.urls', namespace='workflow')),
]
