# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from workflow.apps.workflow.models import Workflow, Project, Item, Changelog

@login_required
def index(request):
    return render(request, 'dashboard/index.haml')


@login_required
def users(request):
    return render(request, 'dashboard/users.haml')


@login_required
def changelog(request):
    return render(request, 'dashboard/changelog.haml', {'posts': Changelog.objects.all()})
