#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire

from django.conf.urls import patterns, url

urlpatterns = patterns('workflow.apps.dashboard',
    url(r'^$', 'views.index', name='index'),
    url(r'^users/', 'views.users', name='users'),
)
