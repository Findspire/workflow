#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, 'index.haml')


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^$', index),
    url(r'^workflow/', include('workflow.apps.workflow.urls', namespace='workflow')),
    url(r'^team/', include('workflow.apps.team.urls', namespace='team')),
]

