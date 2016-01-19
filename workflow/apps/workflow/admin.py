#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire

from django.contrib import admin
from workflow.apps.workflow import models


admin.site.register(models.Comment)
admin.site.register(models.ItemCategory)
admin.site.register(models.ItemModel)
admin.site.register(models.Item)
admin.site.register(models.Project)
admin.site.register(models.Workflow)
admin.site.register(models.Changelog)
