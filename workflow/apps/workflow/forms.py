#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from workflow.apps.workflow.models import Project, ItemModel, ItemCategory, Comment
from workflow.utils.forms import MyMultipleChoiceField, MyCheckboxSelectMultiple


class ProjectNewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'team']

    items = MyMultipleChoiceField(
        choices_data=(ItemCategory, ItemModel),
        widget=MyCheckboxSelectMultiple,
        required=False,
    )


class CommentNewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ItemDetailForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        fields = ['description']
