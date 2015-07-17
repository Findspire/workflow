#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

from workflow.apps.workflow.models import Item, CommentInstanceItem, Person, Validation, Workflow, \
    WorkflowCategory, WorkflowInstance, WorkflowInstanceItem
from workflow.apps.workflow.forms import CommentItemNewForm, DetailItemForm, ItemNewForm, WorkflowInstanceNewForm


@login_required
def index(request):
    return render(request, 'workflow/index.haml')

@login_required
def workflowinstance_new(request):
    if request.method == 'POST':
        form = WorkflowInstanceNewForm(request, data=request.POST)
        if form.is_valid():
            workflow_id = form.cleaned_data['workflow']
            persons = Person.objects.filter(django_user=request.user.id)
            if not len(persons):
                return {"form" : form, "status" : "KO", "error" : "Your django user is not attached to a Team person"}
            if len(get_object_or_404(Workflow, id=workflow_id).leaders.filter(id=persons[0].id)):
                new_workflowinstance = WorkflowInstance(workflow_id=form.cleaned_data['workflow'], version=form.cleaned_data['version'])
                new_workflowinstance.save()
                categories = WorkflowCategory.objects.filter(workflow=workflow_id)
                for category in categories:
                    items = Item.objects.filter(workflow_category=category.id)
                    for item in items:
                        rt = WorkflowInstanceItem(validation=None, item_id=item.id, workflowinstance_id=new_workflowinstance.id)
                        rt.save()
                return HttpResponseRedirect(reverse('workflow:workflowinstance-show', args=[new_workflowinstance.id, 'mine']))
            else:
                return render(request, 'workflow/workflowinstance_new.haml', {"status" : "KO", "error" : "You are not leader on this workflow"})
        else:
            return render(request, 'workflow/workflowinstance_new.haml', {"status" : "KO", "error" : str(form.errors)})
    else:
        form = WorkflowInstanceNewForm(request)

    return render(request, 'workflow/workflowinstance_new.haml', {'form' : form, "status" : "NEW"})


@login_required
def workflowinstance_list(request):
    workflows = Workflow.objects.all()

    ret = {
        'workflows' : [],
    }

    for workflow in workflows:
        ret['workflows'].append({
            'name': workflow,
            'workflowinstances': WorkflowInstance.objects.filter(workflow=workflow),
        })

    return render(request, 'workflow/workflowinstance_list.haml', ret)


@login_required
def check_state_before_change(request, item_id, category_id):
    """ Check if @item_id@ or @category_id@ have changed before change anything
    """
    if int(item_id):
        item = get_object_or_404(WorkflowInstanceItem, id=item_id)
        data = {
            "assigned_to": item.assigned_to_id or "None",
            "validation": (item.validation_id == 1) and "OK" or (item.validation_id == 2) and "KO" or "None",
            "item_id": item_id,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"category_id" : category_id})


@login_required
def workflowinstance_show(request, workflowinstance_id, which_display):
    workflowinstanceitems = WorkflowInstanceItem.objects.filter(workflowinstance=workflowinstance_id)
    person = get_object_or_404(Person, django_user=request.user)

    display = {
        'mine': 'mine',
        'all': 'all',
        'successful': 'successful',
        'failed': 'failed',
        'untaken': 'untaken',
        'taken': 'taken',
    }
    counter = {
        'Total': len(workflowinstanceitems),
        'Success': 0,
        'Failed': 0,
        'Taken': 0,
        'Free': 0,
        'NotSolved': 0,
        'Mine': 0,
    }
    container = {
        'mine' : {},
        'successful': {},
        'failed': {},
        'untaken': {},
        'taken': {},
        'all': {},
    }

    if not which_display in container.keys():
        which_display = "all"

    for workflowinstanceitem in workflowinstanceitems:
        category_id = workflowinstanceitem.item.workflow_category.id
        default_dic = {
            'id' : category_id,
            'name' : workflowinstanceitem.item.workflow_category.name,
            'workflowinstanceitems': {
                workflowinstanceitem.id: workflowinstanceitem
            },
        }

        container["all"].setdefault(category_id, default_dic)

        if workflowinstanceitem.assigned_to == None:
            container["untaken"].setdefault(category_id, default_dic)
            counter['Free'] += 1
        else:
            container["taken"].setdefault(category_id, default_dic)
            counter['Taken'] += 1

            if workflowinstanceitem.assigned_to == person:
                container["mine"].setdefault(category_id, default_dic)
                counter['Mine'] += 1

        if workflowinstanceitem.validation_id == None:
            counter['NotSolved'] += 1
        elif workflowinstanceitem.validation_id == 1:
            container["successful"].setdefault(category_id, default_dic)
            counter['Success'] += 1
        elif workflowinstanceitem.validation_id == 2:
            container["failed"].setdefault(category_id, default_dic)
            counter['Failed'] += 1

    for category in container[which_display]:
        container[which_display][category]['workflowinstanceitems'] = container[which_display][category]['workflowinstanceitems'].values()

    return_d = {
        'validations': Validation.objects.all(),
        'categories': container["all"].values(),
        'workflowinstance': get_object_or_404(WorkflowInstance, id=workflowinstance_id),
        'display': display,
        'counter': counter,
        'categories' : len(container[which_display]) and container[which_display].values() or None,
    }

    return render(request, 'workflow/workflowinstance_show.haml', return_d)


@login_required
def workflowinstance_delete(request, workflowinstance_id):
    WorkflowInstance.objects.filter(id=workflowinstance_id).delete()
    return HttpResponseRedirect(reverse('workflow:workflowinstance-list'))


def workflowinstanceitem_assign_to_person(workflowinstanceitem, person):
    """ Change item assignation and save into db """
    workflowinstanceitem.assigned_to = person
    workflowinstanceitem.save()


@login_required
def workflowinstanceitem_take(request, workflowinstanceitem_id):
    """ Output JSON for AJAX interaction
        Set owner on @workflowinstanceitem_id@
        Return @workflowinstanceitem_id@
    """
    workflowinstanceitem = get_object_or_404(WorkflowInstanceItem, id=workflowinstanceitem_id)
    person = get_object_or_404(Person.objects, django_user=request.user)
    workflowinstanceitem_assign_to_person(workflowinstanceitem, person)
    return JsonResponse({"item_id" : workflowinstanceitem_id, "assigned_to_firstname" : str(person.firstname), "assigned_to_lastname" : str(person.lastname), "assigned_to" : person.id or "None"})


@login_required
def workflowinstanceitem_untake(request, workflowinstanceitem_id):
    """ Output JSON for AJAX interaction
        Reset owner one @workflowinstanceitem_id@
        Return @workflowinstanceitem_id@
    """
    workflowinstanceitem = get_object_or_404(WorkflowInstanceItem, id=workflowinstanceitem_id)
    workflowinstanceitem.assigned_to = None
    workflowinstanceitem.save()
    return JsonResponse({"item_id" : workflowinstanceitem_id, "assigned_to" : workflowinstanceitem.assigned_to_id or "None"})


@login_required
def workflowinstance_take_category(request, workflowinstance_id, category_id):
    """ Output JSON for AJAX interaction
        Set owner on concerned items
        Return the category_id of item concerned and owner's lastname and firstname
    """
    items = WorkflowInstanceItem.objects.filter(workflowinstance__id=workflowinstance_id)
    person = get_object_or_404(Person, django_user=request.user)
    for item in items:
        if item.item.workflow_category.id == int(category_id) and not item.assigned_to_id:
            workflowinstanceitem_assign_to_person(item, person)
    return JsonResponse({"category_id" : category_id, "assigned_to_firstname" : str(person.firstname), "assigned_to_lastname" : str(person.lastname), "assigned_to" : person.id})


@login_required
def workflowinstance_untake_category(request, workflowinstance_id, category_id):
    """ Output JSON for AJAX interaction
        Reset owner on concerned items
        Return the category_id of item
    """
    items = WorkflowInstanceItem.objects.filter(workflowinstance__id=workflowinstance_id)
    person = get_object_or_404(Person, django_user=request.user.id)
    for item in items:
        if item.item.workflow_category.id == int(category_id) and item.assigned_to_id == person.id:
            workflowinstanceitem_assign_to_person(item, None)
    return JsonResponse({"category_id" : category_id, "person_id" : person.id})


@login_required
def workflowinstanceitem_validate(request, workflowinstanceitem_id, validation_label):
    """ Output JSON for AJAX interaction
        Change item state: Validate/Invalidate
        Return @workflowinstanceitem_id@ which is the item id
    """
    workflowinstanceitem = get_object_or_404(WorkflowInstanceItem, id=workflowinstanceitem_id)
    workflowinstanceitem.validation_id = validation_label == "OK" and 1 or 2
    workflowinstanceitem.save()
    return JsonResponse({"item_id" : workflowinstanceitem_id})


@login_required
def workflowinstanceitem_no_state(request, workflowinstanceitem_id):
    """ Reset item state
        Return @item_id@
    """
    workflowinstanceitem = get_object_or_404(WorkflowInstanceItem, id=workflowinstanceitem_id)
    workflowinstanceitem.validation_id = None
    workflowinstanceitem.save()
    return JsonResponse({"item_id" : workflowinstanceitem_id})


@login_required
def workflowinstanceitem_show(request, workflowinstanceitem_id):
    """ Create form for comments
        Create form for edit details
        Get information about current item @workflowinstanceitem_id@

        Return dictionnary with all of that
    """
    return_d = {}
    return_d.update(workflowinstanceitem_comments(request, workflowinstanceitem_id))
    return_d.update(workflowinstanceitem_details(request, workflowinstanceitem_id))
    workflowinstanceitem = get_object_or_404(WorkflowInstanceItem, id=workflowinstanceitem_id)
    if workflowinstanceitem.item.details:
        workflowinstanceitem.item.details = workflowinstanceitem.item.details
    else:
        workflowinstanceitem.item.details = []
    comments = CommentInstanceItem.objects.filter(item=workflowinstanceitem_id)
    return_d.update({'workflowinstanceitem' : workflowinstanceitem, 'validations' : Validation.objects.all()})
    return_d.update({'from_item_details' : 'from_item_details', 'comments' : comments, "all" : "all"})
    return render(request, 'workflow/workflowinstanceitem_show.haml', return_d)


def workflowinstanceitem_comments(request, workflowinstanceitem_id):
    """ Return form for comments on specific item """
    if request.method == 'POST':
        person = get_object_or_404(Person, django_user=request.user)
        form = CommentItemNewForm(request, data=request.POST)
        if form.is_valid():
            comment = CommentInstanceItem(comments=form.cleaned_data['comments'], item_id=workflowinstanceitem_id, person=person)
            comment.save()
            form = CommentItemNewForm(request)
            return {'status_comment' : 'OK', 'form_comment' : form}
        else:
            return {'status_comment' : 'KO', 'error' : str(form.errors), 'form_comment' : form}
    else:
        form = CommentItemNewForm(request)
    return {'form_comment' : form}


def workflowinstanceitem_details(request, workflowinstanceitem_id):
    """ Return form for details on specific item """
    workflowinstanceitem = get_object_or_404(WorkflowInstanceItem, id=workflowinstanceitem_id)
    initial_value = workflowinstanceitem.item.details
    if request.method == 'POST' and "_post" in request.POST:
        form = DetailItemForm(request, initialValue='', data=request.POST)
        if form.is_valid():
            workflowcategory = get_object_or_404(WorkflowCategory, id=workflowinstanceitem.item.workflow_category_id)
            detail = Item(id=workflowinstanceitem.item.id, workflow_category=workflowcategory, \
                    label=workflowinstanceitem.item.label, details=form.cleaned_data['details'])
            detail.save()
            form = DetailItemForm(request, initialValue=form.cleaned_data['details'])
            return {'status_detail' : 'OK', 'form_detail' : form}
        else:
            return {'status_detail' : 'KO', 'error' : str(form.errors), 'form_detail' : form}
    elif "_reset" in request.POST:
        workflowinstanceitem = get_object_or_404(WorkflowInstanceItem, id=workflowinstanceitem_id)
        workflowcategory = get_object_or_404(WorkflowCategory, id=workflowinstanceitem.item.workflow_category_id)
        detail = Item(id=workflowinstanceitem.item.id, workflow_category=workflowcategory, \
                    label=workflowinstanceitem.item.label, details='')
        detail.save()
        form = DetailItemForm(request, initialValue='')
        return {'form_detail' : form}
    else:
        form = DetailItemForm(request, initial_value)
    return {'form_detail' : form}


@login_required
def item_new(request):
    if request.method == 'POST':
        form = ItemNewForm(request, data=request.POST)
        if form.is_valid():
            workflowcategory_id = int(form.cleaned_data['category'])
            workflowcategory = get_object_or_404(WorkflowCategory, id=workflowcategory_id)
            workflow = workflowcategory.workflow

            persons = get_object_or_404(Person, django_user=request.user)
            if not persons:
                c = {"form" : form, "status" : "KO", "error" : "Your django user is not attached to a Team person"}
                return render(request, 'workflow/item_new.haml', c)

            if persons in workflow.leaders.all():
                for label in form.cleaned_data['items'].splitlines():
                    label = label.strip()
                    if not label:
                        continue
                    item = Item(workflow_category_id=workflowcategory_id, label=label)
                    item.save()
                c = {"status" : "OK"}
                return render(request, 'workflow/item_new.haml', c)
            else:
                c = {"status" : "KO", "error" : "You are not leader on this workflow"}
                return render(request, 'workflow/item_new.haml', c)

        else:
            c = {"status" : "KO", "error" : str(form.errors)}
            return render(request, 'workflow/item_new.haml', c)
    else:
        form = ItemNewForm(request)

    return render(request, 'workflow/item_new.haml', {'form' : form, "status" : "NEW"})
