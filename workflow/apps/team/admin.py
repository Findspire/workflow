#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from . import models


admin.site.register(models.Person)
admin.site.register(models.Team)
admin.site.register(models.SkillCategory)
admin.site.register(models.SkillSubject)
admin.site.register(models.Skill)
