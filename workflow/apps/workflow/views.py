#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404

from workflow.apps.workflow.models import Comment, ItemCategory, ItemInstance, ItemModel, Person, Project, WorkflowInstance
from workflow.apps.workflow.forms import CommentNewForm, ItemDetailForm, ItemModelNewForm, ProjectNewForm, WorkflowInstanceNewForm


def welcome(request):
    return HttpResponseRedirect(reverse('workflow:index'))


@login_required
def index(request):
    return render(request, 'workflow/index.haml')


@login_required
def project_new(request):
    if request.method == 'POST':
        form = ProjectNewForm(request.POST)
        if form.is_valid():
            p = Project()
            p.name = form.cleaned_data['name']
            p.team = form.cleaned_data['team']
            p.save()  # for the m2m below
            p.items = form.cleaned_data['items']
            p.save()

            return HttpResponseRedirect(reverse('workflow:project_list'))
        else:
            return render(request, 'workflow/project_new.haml', {'form': form})
    else:
        form = ProjectNewForm()

    return render(request, 'workflow/project_new.haml', {'form': form})


@login_required
def project_list(request):
    projects = Project.objects.all()

    context = {
        'projects': {},
    }

    for project in projects:
        context['projects'][project] = WorkflowInstance.objects.filter(project=project)

    return render(request, 'workflow/project_list.haml', context)


@login_required
def workflow_new(request):
    if request.method == 'POST':
        form = WorkflowInstanceNewForm(request.POST)
        if form.is_valid():
            wi = WorkflowInstance()
            wi.project = form.cleaned_data['project']
            wi.version = form.cleaned_data['version']
            wi.save()  # for the m2m below
            wi.items = [ItemInstance.objects.create(item_model=i) for i in form.cleaned_data['items']]
            wi.save()

            return HttpResponseRedirect(reverse('workflow:workflow_show', args=[wi.pk, 'all']))
        else:
            return render(request, 'workflow/workflow_new.haml', {'form': form})
    else:
        form = WorkflowInstanceNewForm()

    return render(request, 'workflow/workflow_new.haml', {'form': form})


@login_required
def workflowinstance_delete(request, workflow_pk):
    WorkflowInstance.objects.filter(id=workflow_pk).delete()
    return HttpResponseRedirect(reverse('workflow:project_list'))


@login_required
def workflow_show(request, workflow_pk, which_display):
    request_person = get_object_or_404(Person, user=request.user)
    workflow = get_object_or_404(WorkflowInstance, pk=workflow_pk)
    items = ItemInstance.objects.filter(workflow=workflow)

    if which_display not in ('all', 'mine', 'untested', 'success', 'failed', 'untaken', 'taken'):
        raise Http404('Unexpected display "%s"' % which_display)

    context = {
        'workflow': workflow,
        'counters': {
            'all': items.count(),
            'mine': 0,
            'untested': 0,
            'success': 0,
            'failed': 0,
            'untaken': 0,
            'taken': 0,
        },
        'percent': {},
        'items': [],
        'ItemInstance': ItemInstance,
    }

    # counters

    for item in items:
        if item.assigned_to == None:
            context['counters']['untaken'] += 1
        else:
            context['counters']['taken'] += 1
            if item.assigned_to == request_person:
                context['counters']['mine'] += 1

        if item.validation == ItemInstance.VALIDATION_UNTESTED:
            context['counters']['untested'] += 1
        elif item.validation == ItemInstance.VALIDATION_SUCCESS:
            context['counters']['success'] += 1
        elif item.validation == ItemInstance.VALIDATION_FAILED:
            context['counters']['failed'] += 1

    for key, count in context['counters'].items():
        context['percent'][key] = 100 * count / (items.count() or 1)

    # shown items

    items_list = {
        'all': items,
        'mine': items.filter(assigned_to=request_person),
        'untested': items.filter(validation=ItemInstance.VALIDATION_UNTESTED),
        'success': items.filter(validation=ItemInstance.VALIDATION_SUCCESS),
        'failed': items.filter(validation=ItemInstance.VALIDATION_FAILED),
        'untaken': items.filter(assigned_to=None),
        'taken': items.exclude(assigned_to=None),
    }[which_display]

    items_dic = {}

    for item in items_list:
        items_dic.setdefault(item.item_model.category.pk, [])
        items_dic[item.item_model.category.pk].append(item)

    for cat_pk, items in items_dic.items():
        context['items'].append([get_object_or_404(ItemCategory, pk=cat_pk), items])

    return render(request, 'workflow/workflow_show.haml', context)


@login_required
def itemmodel_new(request):
    if request.method == 'POST':
        form = ItemModelNewForm(request.POST)
        if form.is_valid():
            im = ItemModel()
            im.name = form.cleaned_data['name']
            im.description = form.cleaned_data['description']
            im.category = form.cleaned_data['category']
            im.save()

            return HttpResponseRedirect('/')
            # todo responseredirect item model list
        else:
            return render(request, 'workflow/itemmodel_new.haml', {'form': form})
    else:
        form = ItemModelNewForm()

    return render(request, 'workflow/itemmodel_new.haml', {'form': form})


@login_required
def iteminstance_show(request, item_pk):
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
                return HttpResponseRedirect(reverse('workflow:iteminstance_show', args=[item.pk]))
        elif '_description' in request.POST:
            form_description = ItemDetailForm(request.POST, initial=model_to_dict(item.item_model))
            if form_description.is_valid():
                item.item_model.description = form_description.cleaned_data['description']
                item.item_model.save()
                return HttpResponseRedirect(reverse('workflow:iteminstance_show', args=[item.pk]))

    context = {
        'item': item,
        'comments': Comment.objects.filter(item=item),
        'form_comment': form_comment,
        'form_description': form_description,
        'ItemInstance': ItemInstance,
    }

    return render(request, 'workflow/iteminstance_show.haml', context)


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
