#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

import workflow.apps.workflow.urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('workflow.apps.workflow.urls')),
]
