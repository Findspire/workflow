#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from braces.views import LoginRequiredMixin

from workflow.utils.generic_views import CreateUpdateView
from .models import CompetenceInstance, CompetenceCategory, CompetenceSubject, Team, Person
from .forms import PersonForm, UserFormCreate, UserFormUpdate


@login_required
def index(request):
    return render(request, 'team/index.haml')


@login_required
def person_handle_form(request, pk=None):
    creating = (pk == None)
    if creating:
        person = Person()
        user = User()
        UserForm = UserFormCreate
    else:
        person = get_object_or_404(Person, pk=pk)
        user = person.user
        UserForm = UserFormUpdate

    if request.method == 'POST':
        person_form = PersonForm(request.POST)
        user_form = UserForm(request.POST)

        if person_form.is_valid() and user_form.is_valid():

            # django user
            if creating:
                user.username = user_form.cleaned_data['username']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()

            # person
            person.arrival_date = person_form.cleaned_data['arrival_date']
            person.contract_type = person_form.cleaned_data['contract_type']
            person.user = user
            person.save()

            # competences
            techno_current = set([c.techno for c in CompetenceInstance.objects.filter(person=person)])
            techno_new = set([get_object_or_404(CompetenceSubject, pk=pk) for pk in person_form.cleaned_data['competences']])

            for techno in techno_current - techno_new:
                comp = get_object_or_404(CompetenceInstance, person=person, techno=techno)
                comp.delete()

            for techno in techno_new - techno_current:
                comp = CompetenceInstance()
                comp.techno = techno
                comp.person = person
                comp.strength = 42
                comp.save()

            return HttpResponseRedirect(reverse('team:person_list'))
    else:
        initial = model_to_dict(person)
        initial.update({'competences': [c.techno.pk for c in CompetenceInstance.objects.filter(person=person)]})
        user_form = UserForm(initial=model_to_dict(user))
        person_form = PersonForm(initial=initial)

    context = {
        'person_form': person_form,
        'user_form': user_form,
        'creating': creating,
        'person_pk': person.pk if person else None,
    }

    if creating:
        context.update({
            'title': 'Person creation',
            'submit': 'Save',
        })
    else:
        context.update({
            'title': 'Person update',
            'submit': 'Update',
        })

    return render(request, 'team/person_form.haml', context)


@login_required
def person_list(request):
    context = {
        'persons': Person.objects.all(),
    }
    return render(request, 'team/person_list.haml', context)


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
        'teams': Team.objects.all().select_related(),
    }
    return render(request, 'team/team_list.haml', context)
