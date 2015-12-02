#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire
from __future__ import unicode_literals


from collections import OrderedDict

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from workflow.utils.generic_views import CreateUpdateView, MyListView
from workflow.apps.workflow.models import Comment, Item, ItemModel, ItemCategory, Project, Workflow
from workflow.apps.workflow.forms import CommentNewForm, ItemDetailForm, ProjectNewForm, WorkflowNewForm, ItemCreateForm
from workflow.apps.workflow.models import update_item_position


@login_required
def index(request):
    return render(request, 'workflow/index.haml')


class ProjectFormView(LoginRequiredMixin, CreateUpdateView):
    model = Project
    form_class = ProjectNewForm
    success_url = reverse_lazy('workflow:project_list')
    template_name = 'utils/workflow_generic_views_form.haml'


@login_required
def project_list(request):
    context = {
        'projects': {project:Workflow.objects.filter(project=project, archived=False) for project in Project.objects.all()},
    }
    return render(request, 'workflow/project_list.haml', context)


class WorkflowFormView(LoginRequiredMixin, CreateUpdateView):
    model = Workflow
    form_class = WorkflowNewForm
    template_name = 'utils/workflow_generic_views_form.haml'


@login_required
def workflow_delete(request, workflow_pk):
    workflow = get_object_or_404(Workflow, pk=workflow_pk)
    if request.user.person is workflow.project.team.leader or request.user.is_superuser:
        workflow.delete()
    else:
        return HttpResponseForbidden(_('You are not allowed to delete this workflow. Contact %s :)' % 
                                     workflow.project.team.leader))
    return redirect('workflow:project_list')


@login_required
def workflow_show(request, workflow_pk, which_display):
    displays = ('all', 'mine', 'untested', 'success', 'failed', 'untaken', 'taken')

    if which_display not in displays:
        raise Http404('Unexpected display "%s"' % which_display)

    request_person = request.user.person
    workflow = get_object_or_404(Workflow, pk=workflow_pk)
    team = workflow.project.team

    if request_person not in team.members.all() and not request.user.is_superuser:
        raise PermissionDenied

    items = set(workflow.get_items(which_display, request_person))
    categories = workflow.categories.all()

    items_by_category = []
    for category in categories:
        cat_items = [item for item in items if item.category_id == category.id]
        items_by_category.append((category, [item for item in sorted(cat_items, key=lambda item: item.position)]))

    context = {
        'workflow': workflow,
        'categories': items_by_category,
        'counters': {display: workflow.get_count(display, request_person) for display in displays},
        'which_display': which_display,
        'Item': Item
    }

    return render(request, 'workflow/workflow_show.haml', context)


class ItemModelFormView(LoginRequiredMixin, CreateUpdateView):
    model = ItemModel
    fields = ['name', 'category', 'description']
    success_url = reverse_lazy('workflow:item_model_list')
    template_name = 'utils/workflow_generic_views_form.haml'


@login_required
def create_item_view(request, category, workflow_pk):
    if request.method == 'POST':
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            items = form.cleaned_data['items']
            workflow = get_object_or_404(Workflow, pk=workflow_pk)
            category = get_object_or_404(ItemCategory, pk=category)
            for name in items.split('\n'):
                if name.strip():
                    item_model, created = ItemModel.objects.get_or_create(name=name, category=category)
                    item = Item.objects.create(item_model=item_model, workflow=workflow)
            return redirect(reverse('workflow:workflow_show', kwargs={'workflow_pk': workflow_pk,
                                                                      'which_display': 'all'}))
        else:
            return HttpResponseForbidden('Informations form are incorrects')
    else:
        return render(request, 'utils/workflow_generic_views_form.haml', {'form': ItemCreateForm()})


@login_required
def delete_comment_view(request, comment_pk, workflow_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect(reverse('workflow:workflow_show', kwargs={'workflow_pk': workflow_pk, 'which_display': 'all'}))


class ItemModelFormViewFromWorkflow(ItemModelFormView):

    def form_valid(self, form):
        ret = super(ItemModelFormViewFromWorkflow, self).form_valid(form)

        # add to newly created ItemModel to the projects and the workflow
        created = form.instance

        workflow = get_object_or_404(Workflow, pk=self.kwargs['workflow_pk'])
        Item.objects.create(item_model=created, workflow=workflow)
        project = workflow.project_set
        project.items.add(created)

        return ret

    def get_success_url(self):
        workflow_pk = self.kwargs['workflow_pk']
        return reverse_lazy('workflow:workflow_show', args=[workflow_pk, 'all'])


class ItemCategoryFormView(LoginRequiredMixin, CreateUpdateView):
    model = ItemCategory
    fields = ['name']
    success_url = reverse_lazy('workflow:index')
    template_name = 'utils/workflow_generic_views_form.haml'

    def form_valid(self, form):
        ret = super(ItemCategoryFormView, self).form_valid(form)
        # if creating a category from a workflow
        if 'workflow_pk' in self.kwargs: # todo: check permissions in team or superuser
            workflow = get_object_or_404(Workflow, pk=self.kwargs['workflow_pk'])
            workflow.categories.add(form.instance)
            get_object_or_404(Project, pk=workflow.project.pk).categories.add(form.instance)
        return ret


@login_required
def item_instance_show(request, item_pk):
    item = get_object_or_404(Item.objects.select_related(), pk=item_pk)

    team = item.workflow.project.team
    if request.user.person not in team.members.all() and not request.user.is_superuser:
        raise PermissionDenied

    # default
    form_comment = CommentNewForm()
    form_description = ItemDetailForm(initial=model_to_dict(item.item_model))

    if request.method == 'POST':
        if request.POST['type'] == 'comment':
            form_comment = CommentNewForm(request.POST)
            if form_comment.is_valid():
                c = Comment()
                c.item = item
                c.person = request.user.person
                c.text = form_comment.cleaned_data['text']
                c.save()
                return HttpResponseRedirect(reverse('workflow:item_instance_show', args=[item.pk]))
        elif request.POST['type'] == 'description':
            form_description = ItemDetailForm(request.POST, initial=model_to_dict(item.item_model))
            if form_description.is_valid():
                item.item_model.description = form_description.cleaned_data['description']
                item.item_model.save()
                return HttpResponseRedirect(reverse('workflow:item_instance_show', args=[item.pk]))

    context = {
        'item': item,
        'comments': Comment.objects.filter(item=item).select_related(),
        'form_comment': form_comment,
        'form_description': form_description,
        'Item': Item,
        'which_display': 'all',
    }

    return render(request, 'workflow/item_instance_show.haml', context)


@login_required
def update(request, which_display, action, model, pk, pk_other=None):
    # todo: this should be a POST request
    if model == 'item':
        item = get_object_or_404(Item, pk=pk)
        workflow_pk = item.workflow.pk

        if action == 'take':
            item.assigned_to = request.user.person
            item.assigned_to_name_cache = request.user.username
        elif action == 'untake':
            if item.validation == 0:
                item.assigned_to = None
                item.assigned_to_name_cache = None
            else:
                return HttpResponseForbidden(_("You need to put this this task has untested '?' before untake it"))
        else:
            raise Http404('Unexpected action "%s"' % action)
        item.save()
        return redirect(reverse('workflow:workflow_show', kwargs={'workflow_pk': workflow_pk, 'which_display': 'all'}))
    else:
        raise Http404('Unexpected model "%s"' % model)

    # response

    if request.is_ajax():
        if model == 'item':
            context = {
                'item': get_object_or_404(Item, pk=pk),
                'which_display': which_display,
            }
            return render(request, 'workflow/workflow_show.take_untake.part.haml', context)
        elif model == 'category':
            workflow = get_object_or_404(Workflow, pk=workflow_pk)
            items = workflow.get_items(which_display, request.user.person).filter(item_model__category__pk=int(pk))

            context = {
                'category': get_object_or_404(ItemCategory, pk=pk),
                'items_list': items,
                'workflow': workflow,
                'Item': Item,
                'which_display': which_display,
            }
            return render(request, 'workflow/workflow_show.table.part.haml', context)
    else:
        default_url = reverse('workflow:workflow_show', args=[workflow_pk, which_display])
        return HttpResponseRedirect(request.GET.get('next', default_url))


@login_required
def update_item_validation(request, item_pk, action):
    item = get_object_or_404(Item, pk=item_pk)
    if item.assigned_to_name_cache != request.user.username:
        if item.assigned_to_name_cache is not None:
            return HttpResponseForbidden(_("%s is the owner of this task" \
                                             % item.assigned_to_name_cache))
        else:
            return HttpResponseForbidden(_("You must take the task before edit it"))
    else:
        status_old = item.validation
        try:
            item.validation = {
                'success': Item.VALIDATION_SUCCESS,
                'failed': Item.VALIDATION_FAILED,
                'untested': Item.VALIDATION_UNTESTED
            }[action]
            item.save()
        except KeyError:
            return Http404(_('Action does not exist'))
        data = {
            'item_pk': item.pk,
            'validation': item.validation,
            'status_old': status_old,
            'updated_at': item.updated_at,
        }
        return JsonResponse(data)


@login_required
def itemmodel_list(request):
    context = {
        'object_list': {cat:ItemModel.objects.filter(category=cat) for cat in ItemCategory.objects.all()}
    }
    return render(request, 'workflow/itemmodel_list.haml', context)


@login_required
@csrf_exempt
def drag_item(request, item_pk, related_pk=None):
    item = get_object_or_404(Item, pk=item_pk)
    if related_pk is not None:
        related_item = Item.objects.get(pk=related_pk)
        update_item_position(item, related_item)
    else:
        update_item_position(item)
    return redirect(reverse('workflow:workflow_show', 
                            kwargs={'workflow_pk': item.workflow.pk, 'which_display': 'all'}))


@login_required
def take_items_category(request, workflow_pk, category_pk, action):
    if action == 'take':
        Item.objects.filter(category__pk=category_pk, assigned_to=None, workflow__pk=workflow_pk)\
                    .update(assigned_to=request.user, assigned_to_name_cache=request.user.username)
    elif action == 'untake':
        Item.objects.filter(category__pk=category_pk, assigned_to_name_cache=request.user.username,
                            validation=0, workflow__pk=workflow_pk)\
                    .update(assigned_to=None, assigned_to_name_cache=None)                     
    else:
        raise Http404('Action %s does not exist' % action)
    return redirect(reverse('workflow:workflow_show', kwargs={'workflow_pk': workflow_pk, 'which_display': 'all'}))

