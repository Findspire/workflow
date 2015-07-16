#!/usr/bin/env python
#-*- coding: utf-8 -*-
#  Copyright 2013 Findspire

'''
Global url patterns for django
'''

from django.conf.urls import patterns, url

from django.conf.urls.defaults import *
import workflow.apps.workflow.urls
from django.contrib import admin
from workflow import settings
from workflow.apps.workflow.models import *
admin.autodiscover()

# And include this URLpattern...
urlpatterns = patterns('',
            # ...
            (r'^admin/', include(admin.site.urls))
)

urlpatterns += workflow.apps.workflow.urls.urlpatterns
