#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict, modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext  as _
from django.views.generic.list import ListView

from braces.views import LoginRequiredMixin

from workflow.utils.generic_views import CreateUpdateView
from workflow.apps.team.models import Skill, SkillCategory, SkillSubject, Team, Person
from workflow.apps.team.forms import TeamNewForm, PersonForm, UserFormCreate, UserFormUpdate


@login_required
def index(request):
    return render(request, 'team/index.haml')


@login_required
def person_handle_form(request, person_pk=None):
    creating = (person_pk == None)
    if creating:
        person = Person()
        user = User()
        UserForm = UserFormCreate
    else:
        person = get_object_or_404(Person, pk=person_pk)
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

            # skills
            techno_current = set([c.techno for c in Skill.objects.filter(person=person)])
            techno_new = set([get_object_or_404(SkillSubject, pk=pk) for pk in person_form.cleaned_data['skills']])

            for techno in techno_current - techno_new:
                comp = get_object_or_404(Skill, person=person, techno=techno)
                comp.delete()

            for techno in techno_new - techno_current:
                comp = Skill()
                comp.techno = techno
                comp.person = person
                comp.strength = settings.COMP_STRENGTH_DEFAULT
                comp.save()

            return HttpResponseRedirect(reverse('team:person_list'))
    else:
        user_form = UserForm(initial=model_to_dict(user))
        initial = model_to_dict(person)
        initial.update({'skills': [c.techno.pk for c in Skill.objects.filter(person=person)]})
        person_form = PersonForm(initial=initial)

    context = {
        'person_form': person_form,
        'user_form': user_form,
        'creating': creating,
        'person': person,
    }

    if creating:
        context.update({
            'title': _('Person creation'),
            'submit': _('Save'),
        })
    else:
        context.update({
            'title': _('Person update'),
            'submit': _('Update'),
        })

    return render(request, 'team/person_form.haml', context)


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    paginate_by = 20


class SkillFormView(LoginRequiredMixin, CreateUpdateView):
    model = Skill
    fields = ['techno', 'person', 'strength']
    template_name = 'utils/team_generic_views_form.haml'

    def get_success_url(self):
        person_pk = self.get_form_kwargs()['data']['person']
        return reverse_lazy('team:skill_instance_list', args=[person_pk])


@login_required
def skills_list(request, person_pk):
    person = get_object_or_404(Person, pk=person_pk)

    MyFormSet = modelformset_factory(Skill, fields=['strength'])

    if request.method == "POST":
        myformset = MyFormSet(request.POST, queryset=Skill.objects.filter(person=person))

        if myformset.is_valid():
            myformset.save()
            return HttpResponseRedirect(reverse('team:person_edit', args=[person_pk]))
    else:
        myformset = MyFormSet(queryset=Skill.objects.filter(person=person))

    # add the techno name - for form display
    for form in myformset:
        if hasattr(form.instance, 'person'):  # not the form for creating a new object
            skill = get_object_or_404(SkillSubject, pk=form.instance.techno.pk)
            form['strength'].label = '{} ({})'.format(skill.name, skill.category.name)
        else:
            form['strength'].label = None

    return render(request, 'team/skill_list.haml', {
        'profile_detail': person,
        'myformset'  : myformset,
    })


class SkillCategoryView(LoginRequiredMixin, CreateUpdateView):
    model = SkillCategory
    fields = ['name']
    success_url = reverse_lazy('team:skill_subject_list')
    template_name = 'utils/team_generic_views_form.haml'


class SkillSubjectView(LoginRequiredMixin, CreateUpdateView):
    model = SkillSubject
    fields = ['name', 'category', 'description']
    success_url = reverse_lazy('team:skill_subject_list')
    template_name = 'utils/team_generic_views_form.haml'


@login_required
def skill_subject_list(request):
    context = {
        'categories': {cat:SkillSubject.objects.filter(category=cat) for cat in SkillCategory.objects.all()},
    }
    return render(request, 'team/skillsubject_list.haml', context)


class TeamView(LoginRequiredMixin, CreateUpdateView):
    model = Team
    form_class = TeamNewForm
    success_url = reverse_lazy('team:team_list')
    template_name = 'utils/team_generic_views_form.haml'


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
