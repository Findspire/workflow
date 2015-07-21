#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'workflow.apps.workflow.views.welcome', name='welcome'),
    url(r'^workflow/', include('workflow.apps.workflow.urls', namespace='workflow')),
]
