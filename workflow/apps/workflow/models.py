#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from ..team.models import Person, Team


class ItemCategory(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return '%s' % (self.name)


class ItemModel(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1000, blank=True, null=True)
    category = models.ForeignKey(ItemCategory)

    def __unicode__(self):
        return '%s - %s' % (self.category, self.name)


class Project(models.Model):
    name = models.CharField(max_length=32)
    team = models.ForeignKey(Team)
    items = models.ManyToManyField(ItemModel, blank=True)

    def __unicode__(self):
        return '%s' % (self.name)


class WorkflowInstance(models.Model):
    project = models.ForeignKey(Project)
    version = models.CharField(max_length=128)
    creation_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return '%s - %s' % (self.project, self.version)

    def get_items(self, which_display, person=None):
        qs = ItemInstance.objects.filter(workflow=self)

        try:
            return {
                'all': qs,
                'mine': qs.filter(assigned_to=person),
                'untested': qs.filter(validation=ItemInstance.VALIDATION_UNTESTED),
                'success': qs.filter(validation=ItemInstance.VALIDATION_SUCCESS),
                'failed': qs.filter(validation=ItemInstance.VALIDATION_FAILED),
                'untaken': qs.filter(assigned_to=None),
                'taken': qs.exclude(assigned_to=None),
            }[which_display]  # OMG this is awesome !
        except KeyError:
            raise ValueError('Unexpected param "%s"' % which_display)

    def get_count(self, which_display, person=None):
        return self.get_items(which_display, person).count()

    def get_percent(self, which_display, person=None):
        value = self.get_count(which_display, person)
        total = self.get_count('all', person)
        return (100 * value / total) if (total != 0) else 100


class ItemInstance(models.Model):
    VALIDATION_UNTESTED = 0
    VALIDATION_SUCCESS = 1
    VALIDATION_FAILED = 2

    VALIDATION_CHOICES = (
        (VALIDATION_UNTESTED, 'Untested'),  # default
        (VALIDATION_SUCCESS, 'Success'),
        (VALIDATION_FAILED, 'Failed'),
    )

    item_model = models.ForeignKey(ItemModel)
    workflow = models.ForeignKey(WorkflowInstance)
    assigned_to = models.ForeignKey(Person, null=True, blank=True)
    validation = models.SmallIntegerField(
        choices=VALIDATION_CHOICES,
        default=0,
    )

    def __unicode__(self):
        return '%s' % (self.item_model)


class Comment(models.Model):
    item = models.ForeignKey(ItemInstance)
    person = models.ForeignKey(Person)
    date = models.DateField(default=timezone.now)
    text = models.TextField(max_length=1000)

    def __unicode__(self):
        return '%s' % (self.text)
