#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.list import ListView

from workflow.utils.generic_views import CreateUpdateView, LoginRequiredMixin
from .models import CompetenceInstance, CompetenceCategory, CompetenceSubject, Team


@login_required
def index(request):
    return render(request, 'team/index.haml')


class CompetenceInstanceView(LoginRequiredMixin, CreateUpdateView):
    model = CompetenceInstance
    fields = ['techno', 'person', 'strength']
    success_url = '/team/competences/list/'


class CompetenceCategoryView(LoginRequiredMixin, CreateUpdateView):
    model = CompetenceCategory
    fields = ['name']
    success_url = '/team/competences/list/'


class CompetenceSubjectView(LoginRequiredMixin, CreateUpdateView):
    model = CompetenceSubject
    fields = ['name', 'category', 'description']
    success_url = '/team/competences/list/'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        ret = self.initial.copy()
        category_pk = self.kwargs.get('category_pk', None)
        if category_pk is not None:  # new competence with assigned subject, set its pk for the form
            ret['category'] = category_pk
        return ret


@login_required
def competences_list(request):
    categories = CompetenceCategory.objects.all()

    context = {
        'categories': {},
    }

    for cat in categories:
        context['categories'][cat] = CompetenceSubject.objects.filter(category=cat)

    return render(request, 'team/competences_list.haml', context)


class TeamView(LoginRequiredMixin, CreateUpdateView):
    model = Team
    fields = ['name', 'leader', 'members']
    success_url = '/team/team/list/'


@login_required
def team_list(request):
    context = {
        'teams': Team.objects.select_related(),
    }

    return render(request, 'team/team_list.haml', context)
