#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire
from __future__ import unicode_literals

from django import forms
from workflow.apps.workflow.models import Project, ItemModel, ItemCategory, Comment, Workflow


class ProjectNewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'team', 'categories']
        widgets = {
            'categories': forms.widgets.CheckboxSelectMultiple,
        }


class WorkflowNewForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = ['project', 'name']


class CommentNewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ItemDetailForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        fields = ['description']


class ItemCreateForm(forms.Form):
    items = forms.CharField(widget=forms.Textarea)
