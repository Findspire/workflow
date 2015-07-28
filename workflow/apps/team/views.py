#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from workflow.utils.generic_views import CreateUpdateView, LoginRequiredMixin
from .models import CompetenceInstance, CompetenceCategory, CompetenceSubject, Team


@login_required
def index(request):
    return render(request, 'team/index.haml')


class CompetenceInstanceView(LoginRequiredMixin, CreateUpdateView):
    model = CompetenceInstance
    fields = ['techno', 'person', 'strength']
    success_url = reverse_lazy('team:competence_subject_list')


class CompetenceCategoryView(LoginRequiredMixin, CreateUpdateView):
    model = CompetenceCategory
    fields = ['name']
    success_url = reverse_lazy('team:competence_subject_list')


class CompetenceSubjectView(LoginRequiredMixin, CreateUpdateView):
    model = CompetenceSubject
    fields = ['name', 'category', 'description']
    success_url = reverse_lazy('team:competence_subject_list')


@login_required
def competence_subject_list(request):
    context = {
        'categories': {cat:CompetenceSubject.objects.filter(category=cat) for cat in CompetenceCategory.objects.all()},
    }
    return render(request, 'team/competences_list.haml', context)


class TeamView(LoginRequiredMixin, CreateUpdateView):
    model = Team
    fields = ['name', 'leader', 'members']
    success_url = reverse_lazy('team:team_list')


@login_required
def team_list(request):
    context = {
        'teams': Team.objects.select_related(),
    }
    return render(request, 'team/team_list.haml', context)
