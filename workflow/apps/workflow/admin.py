#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from workflow.apps.workflow import models

class WorkflowAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Workflow, WorkflowAdmin)

class WorkflowCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.WorkflowCategory, WorkflowCategoryAdmin)

class WorkflowInstanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.WorkflowInstance, WorkflowInstanceAdmin)

class ItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Item, ItemAdmin)

class ValidationAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Validation, ValidationAdmin)

class WorkflowInstanceItemsAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.WorkflowInstanceItem, WorkflowInstanceItemsAdmin)

class ContractTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.ContractType, ContractTypeAdmin)

class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Person, PersonAdmin)

class TeamAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Team, TeamAdmin)

class TeamPersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.TeamPerson, TeamPersonAdmin)

class CompetencesSubjectCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CompetencesSubjectCategory, CompetencesSubjectCategoryAdmin)

class CompetencesSubjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CompetencesSubject, CompetencesSubjectAdmin)

class CompetencesTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CompetencesType, CompetencesTypeAdmin)

class CompetenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Competence, CompetenceAdmin)

class CommentInstanceItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CommentInstanceItem, CommentInstanceItemAdmin)
