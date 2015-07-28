#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import Project, ItemModel, ItemCategory, Comment


class MyCheckboxFieldRenderer(forms.widgets.CheckboxFieldRenderer):
    inner_html = '<li><label>{choice_value}</label>{sub_widgets}</li>'


class MyCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
    renderer = MyCheckboxFieldRenderer


class ProjectNewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'team', 'items']

    choices = []
    for cat in ItemCategory.objects.order_by('name'):
        queryset = ItemModel.objects.filter(category=cat).order_by('name')
        choices_tmp = [(c.pk, c.name) for c in queryset]
        choices.append((cat.name, choices_tmp))

    items = forms.MultipleChoiceField(
        choices=choices,
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
