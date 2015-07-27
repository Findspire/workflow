#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.list import ListView

from .views_generic import CreateUpdateView, LoginRequiredMixin
from .models import CompetenceInstance, CompetenceCategory, CompetenceSubject

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

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        ret = self.initial.copy()
        category_pk = self.kwargs.get('category_pk', None)
        if category_pk is not None:  # new competence with assigned subject, set its pk for the form
            ret['category'] = category_pk
        return ret

    def get_bonus_context_data(self):
        return {
            'title': 'Competence subject ' + ('update' if self.is_update_request() else 'creation'),
        }


@login_required
def competences_list(request):
    categories = CompetenceCategory.objects.all()

    context = {
        'categories': {},
    }

    for cat in categories:
        context['categories'][cat] = CompetenceSubject.objects.filter(category=cat)

    return render(request, 'team/competences_list.haml', context)
