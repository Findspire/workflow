#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire

from django.contrib import admin
from workflow.apps.team import models


admin.site.register(models.Person)
admin.site.register(models.Team)
admin.site.register(models.SkillCategory)
admin.site.register(models.SkillSubject)
admin.site.register(models.Skill)
