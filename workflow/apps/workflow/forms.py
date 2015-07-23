#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from workflow.apps.workflow.models import Project, WorkflowInstance, ItemModel, ItemInstance, Comment, ItemModel

from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import format_html, html_safe
from django.utils.safestring import mark_safe


@html_safe
@python_2_unicode_compatible
class MyChoiceFieldRenderer(object):
    """
    An object used by RadioSelect to enable customization of radio widgets.
    """

    choice_input_class = None
    outer_html = '<ul{id_attr} class="category">{content}</ul>'
    inner_html = '<li>{choice_value}{sub_widgets}</li>'

    def __init__(self, name, value, attrs, choices):
        self.name = name
        self.value = value
        self.attrs = attrs
        self.choices = choices

    def __getitem__(self, idx):
        choice = self.choices[idx]  # Let the IndexError propagate
        return self.choice_input_class(self.name, self.value, self.attrs.copy(), choice, idx)

    def __str__(self):
        return self.render()

    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        id_ = self.attrs.get('id', None)
        output = []
        old_category = None
        for i, choice in enumerate(self.choices):
            choice_value, choice_label = choice

            current_category = choice_label.split('-')[0].strip()
            if old_category != current_category:
                if old_category != None:
                    output.append('</li></ul>')
                output.append('<li><label><input type="checkbox" /> %s</label><ul>' % current_category)
                old_category = current_category

            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{}'.format(i)
                sub_ul_renderer = ChoiceFieldRenderer(name=self.name,
                                                      value=self.value,
                                                      attrs=attrs_plus,
                                                      choices=choice_label)
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html(self.inner_html, choice_value=choice_value, sub_widgets=sub_ul_renderer.render()))
            else:
                w = self.choice_input_class(self.name, self.value, self.attrs.copy(), choice, i)
                output.append(format_html(self.inner_html, choice_value=force_text(w), sub_widgets=''))
        return format_html(self.outer_html,
                           id_attr=format_html(' id="{}"', id_) if id_ else '',
                           content=mark_safe('\n'.join(output)))


class CheckboxFieldRenderer(MyChoiceFieldRenderer):
    choice_input_class = forms.widgets.CheckboxChoiceInput

class MyCheckboxSelectMultiple(forms.widgets.RendererMixin, forms.widgets.SelectMultiple):
    renderer = CheckboxFieldRenderer
    _empty_value = []


class ProjectNewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'team', 'items']
    items = forms.ModelMultipleChoiceField(queryset=ItemModel.objects.order_by('category__name', 'name'), \
        required=False, widget=MyCheckboxSelectMultiple)


class WorkflowInstanceNewForm(forms.ModelForm):
    class Meta:
        model = WorkflowInstance
        fields = ['project', 'version', 'items']
    items = forms.ModelMultipleChoiceField(queryset=ItemModel.objects.order_by('category__name', 'name'), \
        required=False, widget=MyCheckboxSelectMultiple)


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
