#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from . import models


admin.site.register(models.Comment)
admin.site.register(models.ItemCategory)
admin.site.register(models.ItemModel)
admin.site.register(models.ItemInstance)
admin.site.register(models.Project)
admin.site.register(models.WorkflowInstance)
