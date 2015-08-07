#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class MyCheckboxFieldRenderer(forms.widgets.CheckboxFieldRenderer):
    """Add the html label tag for further css and js styling"""
    inner_html = '<li><label>{choice_value}</label>{sub_widgets}</li>'


class MyCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
    renderer = MyCheckboxFieldRenderer


class MyMultipleChoiceField(forms.MultipleChoiceField):
    """Implement a nested MultipleChoiceField."""

    def get_choices(self):
        Category, Object = self.choices_data
        choices = []
        for cat in Category.objects.order_by('name'):
            queryset = Object.objects.filter(category=cat).order_by('name')
            choices_tmp = [(c.pk, c.name) for c in queryset]
            choices.append((cat.name, choices_tmp))
        return choices

    def __init__(self, choices_data, *args, **kwargs):
        self.choices_data = choices_data
        super(MyMultipleChoiceField, self).__init__(choices=self.get_choices, *args, **kwargs)
