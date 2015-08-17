#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from workflow.apps.workflow.models import Project, ItemModel, ItemCategory, Comment
from workflow.utils.forms import MyMultipleChoiceField


class ProjectNewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'team']

    items = MyMultipleChoiceField(
        choices_data=(ItemCategory, ItemModel),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        # Initial data only if the form is built from an instance (otherwise, the list should be empty)
        if ('instance' in kwargs) and (kwargs['instance'] is not None):
            kwargs.setdefault('initial', {})
            kwargs['initial']['items'] = [item.pk for item in kwargs['instance'].items.all()]

        super(ProjectNewForm, self).__init__(*args, **kwargs)


class CommentNewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ItemDetailForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        fields = ['description']
