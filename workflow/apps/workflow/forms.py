#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from workflow.apps.workflow.models import Project, WorkflowInstance, ItemModel, ItemInstance, Comment, ItemModel


class ProjectNewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'team', 'items']
    items = forms.ModelMultipleChoiceField(queryset=ItemModel.objects.order_by('category__name', 'name'), required=False)


class WorkflowInstanceNewForm(forms.ModelForm):
    class Meta:
        model = WorkflowInstance
        fields = ['project', 'version', 'items']
    items = forms.ModelMultipleChoiceField(queryset=ItemModel.objects.order_by('category__name', 'name'))


class ItemModelNewForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        fields = ['name', 'description', 'category']


class ItemInstanceNewForm(forms.ModelForm):
    class Meta:
        model = ItemInstance
        fields = ['item_model', 'assigned_to', 'validation']


class CommentNewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ItemDetailForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        fields = ['description']
