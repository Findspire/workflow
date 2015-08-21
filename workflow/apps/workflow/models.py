#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire

"""

A Project has several ItemModel that needs to be done.
When a new version of a Project is planed to be released, a Workflow is created.
For each ItemModel, an Item is created whith a ForeignKey to this ItemModel.
Some Person will be assigned to this Item and will have to mark the validation
state : success or failed (or by default untested).

"""

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy  as _

from workflow.apps.team.models import Person, Team


class ItemCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Name'))

    def __unicode__(self):
        return '%s' % (self.name)


class ItemModel(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_('Description'))
    category = models.ForeignKey(ItemCategory, verbose_name=_('Category'))

    def __unicode__(self):
        return '%s - %s' % (self.category, self.name)


class Project(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('Name'))
    team = models.ForeignKey(Team, verbose_name=_('Team'))
    items = models.ManyToManyField(ItemModel, blank=True, verbose_name=_('Items'))

    def __unicode__(self):
        return '%s' % (self.name)


class Workflow(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('Project'))
    version = models.CharField(max_length=128, verbose_name=_('Version'))
    creation_date = models.DateField(auto_now=True, verbose_name=_('Creation date'))
    categories = models.ManyToManyField(ItemCategory, blank=True, verbose_name=_('Categories'))

    def __unicode__(self):
        return '%s - %s' % (self.project, self.version)

    def get_items(self, which_display, person=None):
        qs = Item.objects \
            .filter(workflow=self, item_model__category__in=self.categories.all()) \
            .order_by('item_model__category__name', 'item_model__name') \
            .select_related('item_model__category', 'assigned_to__user')

        try:
            return {
                'all': qs,
                'mine': qs.filter(assigned_to=person),
                'untested': qs.filter(validation=Item.VALIDATION_UNTESTED),
                'success': qs.filter(validation=Item.VALIDATION_SUCCESS),
                'failed': qs.filter(validation=Item.VALIDATION_FAILED),
                'untaken': qs.filter(assigned_to=None),
                'taken': qs.exclude(assigned_to=None),
            }[which_display]  # OMG this is awesome !
        except KeyError:
            raise ValueError('Unexpected param "%s"' % which_display)

    def get_count(self, which_display, person=None):
        return self.get_items(which_display, person).count()

    def success_percent(self):
        value = self.get_count('success')
        total = self.get_count('all')
        return (100 * value / total) if (total != 0) else 100

    def get_absolute_url(self):
        return reverse('workflow:workflow_show', args=[self.pk, 'all'])

    def save(self, *args, **kwargs):
        pk = self.pk

        # save Workflow first, to have the pk for the later foreignkey from Item - if needed
        super(Workflow, self).save(*args, **kwargs)

        # if the object is created and not updated, create its Items
        if pk == None:
            for item in self.project.items.all():
                Item.objects.create(item_model=item, workflow=self)


class Item(models.Model):
    VALIDATION_UNTESTED = 0
    VALIDATION_SUCCESS = 1
    VALIDATION_FAILED = 2

    VALIDATION_CHOICES = (
        (VALIDATION_UNTESTED, _('Untested')),  # default
        (VALIDATION_SUCCESS, _('Success')),
        (VALIDATION_FAILED, _('Failed')),
    )

    item_model = models.ForeignKey(ItemModel, verbose_name=_('Item model'))
    workflow = models.ForeignKey(Workflow, verbose_name=_('Workflow'))
    assigned_to = models.ForeignKey(Person, null=True, blank=True, verbose_name=_('Assigned to'))
    validation = models.SmallIntegerField(
        choices=VALIDATION_CHOICES,
        default=0,
        verbose_name=_('Validation'),
    )

    def __unicode__(self):
        return '%s' % (self.item_model)


class Comment(models.Model):
    item = models.ForeignKey(Item, verbose_name=_('Item'))
    person = models.ForeignKey(Person, verbose_name=_('Person'))
    date = models.DateField(default=timezone.now, verbose_name=_('Date'))
    text = models.TextField(max_length=1000, verbose_name=_('Text'))

    def __unicode__(self):
        return '%s' % (self.text)
