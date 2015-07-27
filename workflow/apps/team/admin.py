#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from . import models


admin.site.register(models.ContractType)
admin.site.register(models.Person)
admin.site.register(models.Team)
admin.site.register(models.CompetenceCategory)
admin.site.register(models.CompetenceSubject)
admin.site.register(models.CompetenceInstance)
