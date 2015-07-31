#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from .models import Person, CompetenceSubject, CompetenceInstance, CompetenceCategory
from ...utils.forms import MyMultipleChoiceField, MyCheckboxSelectMultiple


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['arrival_date', 'contract_type']

    competences = MyMultipleChoiceField(
        choices_data=(CompetenceCategory, CompetenceSubject),
        widget=MyCheckboxSelectMultiple,
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
