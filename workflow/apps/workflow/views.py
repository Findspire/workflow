#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404

from braces.views import LoginRequiredMixin, GroupRequiredMixin

from workflow.utils.generic_views import CreateUpdateView
from .models import Comment, ItemInstance, ItemModel, ItemCategory, Project, WorkflowInstance
from ..team.models import Person
from .forms import CommentNewForm, ItemDetailForm, ProjectNewForm


@login_required
def index(request):
    return render(request, 'workflow/index.haml')


class ProjectFormView(LoginRequiredMixin, CreateUpdateView):
    model = Project
    form_class = ProjectNewForm
    success_url = reverse_lazy('workflow:project_list')


@login_required
def project_list(request):
    context = {
        'projects': {project:WorkflowInstance.objects.filter(project=project) for project in Project.objects.all()}
    }
    return render(request, 'workflow/project_list.haml', context)


class WorkflowFormView(LoginRequiredMixin, CreateUpdateView):
    model = WorkflowInstance
    fields = ['project', 'version']


@login_required
def workflow_show(request, workflow_pk, which_display):
    displays = ('all', 'mine', 'untested', 'success', 'failed', 'untaken', 'taken')

    if which_display not in displays:
        raise Http404('Unexpected display "%s"' % which_display)

    request_person = get_object_or_404(Person, user=request.user)
    workflow = get_object_or_404(WorkflowInstance, pk=workflow_pk)

    # group by category
    items_list = workflow.get_items(which_display, request_person)
    items_dic = {}
    for item in items_list:
        items_dic.setdefault(item.item_model.category, [])
        items_dic[item.item_model.category].append(item)

    context = {
        'workflow': workflow,
        'counters': {display: workflow.get_count(display, request_person) for display in displays},
        'percent': {display: workflow.get_percent(display, request_person) for display in displays},
        'items': items_dic,
        'ItemInstance': ItemInstance,
    }

    return render(request, 'workflow/workflow_show.haml', context)


class ItemModelFormView(LoginRequiredMixin, CreateUpdateView):
    model = ItemModel
    fields = ['name', 'category', 'description']
    success_url = reverse_lazy('workflow:project_list')


class ItemCategoryFormView(LoginRequiredMixin, CreateUpdateView):
    model = ItemCategory
    fields = ['name']
    success_url = reverse_lazy('workflow:project_list')


@login_required
def item_instance_show(request, item_pk):
    item = get_object_or_404(ItemInstance, id=item_pk)

    # default
    form_comment = CommentNewForm()
    form_description = ItemDetailForm(initial=model_to_dict(item.item_model))

    if request.method == 'POST':
        if '_comment' in request.POST:
            form_comment = CommentNewForm(request.POST)
            if form_comment.is_valid():
                c = Comment()
                c.item = item
                c.person = get_object_or_404(Person, user=request.user)
                c.text = form_comment.cleaned_data['text']
                c.save()
                return HttpResponseRedirect(reverse('workflow:item_instance_show', args=[item.pk]))
        elif '_description' in request.POST:
            form_description = ItemDetailForm(request.POST, initial=model_to_dict(item.item_model))
            if form_description.is_valid():
                item.item_model.description = form_description.cleaned_data['description']
                item.item_model.save()
                return HttpResponseRedirect(reverse('workflow:item_instance_show', args=[item.pk]))

    context = {
        'item': item,
        'comments': Comment.objects.filter(item=item),
        'form_comment': form_comment,
        'form_description': form_description,
        'ItemInstance': ItemInstance,
    }

    return render(request, 'workflow/item_instance_show.haml', context)


@login_required
def update(request, action, model, pk, pk_other=None):
    if model not in ('item', 'category', 'validate'):
        raise Http404('Unexpected model "%s"' % model)

    if model == 'item':
        if action not in ('take', 'untake'):
            raise Http404('Unexpected action "%s"' % action)

        item = get_object_or_404(ItemInstance, pk=pk)
        workflow_pk = item.workflow.pk

        if action == 'take':
            item.assigned_to = get_object_or_404(Person, user=request.user)
        else:  # untake
            item.assigned_to = None

        item.save()
    elif model == 'category':
        if action not in ('take', 'untake'):
            raise Http404('Unexpected action "%s"' % action)

        if action == 'take':
            assigned_to = get_object_or_404(Person, user=request.user)
        else:  # untake
            assigned_to = None

        items = get_list_or_404(ItemInstance, workflow__pk=pk_other)
        for item in items:
            if item.item_model.category.pk == int(pk):
                item.assigned_to = assigned_to
                item.save()

        workflow_pk = pk_other
    elif model == 'validate':
        if action not in ('untested', 'success', 'failed'):
            raise Http404('Unexpected action "%s"' % action)

        item = get_object_or_404(ItemInstance, pk=pk)
        workflow_pk = item.workflow.pk

        if action == 'untested':
            item.validation = ItemInstance.VALIDATION_UNTESTED
        elif action == 'success':
            item.validation = ItemInstance.VALIDATION_SUCCESS
        elif action == 'failed':
            item.validation = ItemInstance.VALIDATION_FAILED

        item.save()

    default_url = reverse('workflow:workflow_show', args=[workflow_pk, 'all'])
    return HttpResponseRedirect(request.GET.get('next', default_url))


@login_required
def item_model_list(request):
    context = {
        'categories': {cat:ItemModel.objects.filter(category=cat) for cat in ItemCategory.objects.all()},
    }
    return render(request, 'workflow/item_list.haml', context)
