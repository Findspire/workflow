#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from workflow.apps.workflow import models


admin.site.register(models.ContractType)
admin.site.register(models.Comment)
admin.site.register(models.Person)
admin.site.register(models.Team)
admin.site.register(models.CompetenceCategory)
admin.site.register(models.CompetenceSubject)
admin.site.register(models.CompetenceInstance)
admin.site.register(models.ItemCategory)
admin.site.register(models.ItemModel)
admin.site.register(models.ItemInstance)
admin.site.register(models.Project)
admin.site.register(models.WorkflowInstance)
