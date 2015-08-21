#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire

from django import forms
from django.contrib.auth.models import User
from workflow.apps.team.models import Team, Person, SkillSubject, SkillCategory
from workflow.utils.forms import MyMultipleChoiceField


class TeamNewForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'leader', 'members']
        widgets = {
            'members': forms.widgets.CheckboxSelectMultiple,
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['arrival_date', 'contract_type']

    skills = MyMultipleChoiceField(
        choices_data=(SkillCategory, SkillSubject),
        required=False,
    )


class UserFormCreate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserFormUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
