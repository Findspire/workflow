#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.list import ListView
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.decorators import method_decorator

from django.core.urlresolvers import reverse

from .views_generic import CreateUpdateView, LoginRequiredMixin
from .models import CompetenceCategory, CompetenceSubject, CompetenceInstance
from .forms import CompetenceCategoryForm, CompetenceSubjectForm, CompetenceInstanceForm


@login_required
def index(request):
    return render(request, 'team/index.haml')


class CompetenceInstanceView(LoginRequiredMixin, CreateUpdateView):
    model = CompetenceInstance
    fields = ['techno', 'person', 'strength']

    def get_bonus_context_data(self):
        return {
            'title': 'Competence instance ' + ('update' if self.is_update_request() else 'creation'),
        }


class CompetenceCategoryView(LoginRequiredMixin, CreateUpdateView):
    model = CompetenceCategory
    fields = ['name']

    def get_bonus_context_data(self):
        return {
            'title': 'Competence category ' + ('update' if self.is_update_request() else 'creation'),
        }


class CompetenceSubjectView(LoginRequiredMixin, CreateUpdateView):
    model = CompetenceSubject
    fields = ['name', 'category', 'description']

    def get_bonus_context_data(self):
        return {
            'title': 'Competence subject ' + ('update' if self.is_update_request() else 'creation'),
        }


class CompetenceInstanceListView(ListView):
    model = CompetenceInstance
    template_name = 'team/competence_instance_list.haml'


class CompetenceCategoryListView(ListView):
    model = CompetenceCategory
    template_name = 'team/competence_category_list.haml'


class CompetenceSubjectListView(ListView):
    model = CompetenceSubject
    template_name = 'team/competence_subject_list.haml'

