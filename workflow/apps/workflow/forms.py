#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire
from __future__ import unicode_literals

from django import forms
from workflow.apps.workflow.models import Project, ItemModel, ItemCategory, Comment, Workflow


class WorkflowNewForm(forms.ModelForm):
    WORKFLOW_CHOICES = [(workflow.id, workflow.name) for workflow in Workflow.objects.all()]
    workflow_base = forms.BooleanField()
    workflow_model = forms.ChoiceField(choices=WORKFLOW_CHOICES)

    class Meta:
        model = Workflow
        fields = ['project', 'name', 'workflow_base', 'workflow_model']


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
