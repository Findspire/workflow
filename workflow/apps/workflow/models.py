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
from django.db.models import F
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy  as _


from workflow.apps.team.models import Person, Team


class Changelog(models.Model):
    title = models.CharField(default=_("Title"), max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        verbose_name = "Changelog"
        verbose_name_plural = "Changelog"
        ordering = ['created_at']

    def __str__(self):
        return self.title

class ItemCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    position = models.IntegerField(null=True, editable=False)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return '%s' % (self.name)

    def get_items(self):
        return self.item_set.all()

@receiver(post_delete, sender=ItemCategory)
def delete_items_category(sender, instance=None, **kwargs):
    for item in instance.get_items():
        item.delete()

def update_category_position(workflow, category, related_category=None):
    if related_category is not None:
        category.position = related_category.position
        categories = workflow.categories.all().filter(position__gte=category.position)\
                                              .update(position=F('position') + 1)
    else:
        related_category = workflow.categories.all().last()
        category.position = related_category.position + 1 if related_category.position else 0
    category.save()


class ItemModel(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_('Description'))
    category = models.ForeignKey(ItemCategory, verbose_name=_('Category'))

    def __unicode__(self):
        return '%s - %s' % (self.category, self.name)


class Project(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('Name'))
    team = models.ForeignKey(Team, verbose_name=_('Team'))

    def __unicode__(self):
        return '%s' % (self.name)


class Workflow(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('Project'))
    name = models.CharField(max_length=128, verbose_name=_('Version'))
    creation_date = models.DateField(auto_now=True, verbose_name=_('Creation date'))
    categories = models.ManyToManyField(ItemCategory, blank=True, verbose_name=_('Categories'))
    archived = models.BooleanField(default=False)
    position = models.IntegerField(null=True, editable=False)
    success = models.IntegerField(default=0, editable=False)
    untested = models.IntegerField(default=0, editable=False)
    failed = models.IntegerField(default=0, editable=False)
    disabled = models.IntegerField(default=0, editable=False)
    total = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return '%s - %s' % (self.project, self.name)

    def get_items(self, which_display, person=None):
        qs = Item.objects \
            .filter(workflow=self, category__in=self.categories.all()) \
            .order_by('position') \
            .select_related('category', 'assigned_to__user')
        try:
            return {
                'all': qs,
                'mine': qs.filter(assigned_to_name_cache=person),
                'untested': qs.filter(validation=Item.VALIDATION_UNTESTED),
                'success': qs.filter(validation=Item.VALIDATION_SUCCESS),
                'failed': qs.filter(validation=Item.VALIDATION_FAILED),
                'disabled': qs.filter(validation=Item.VALIDATION_DISABLED),
                'untaken': qs.filter(assigned_to=None),
                'taken': qs.exclude(assigned_to=None),
            }[which_display]
        except KeyError:
            raise ValueError('Unexpected param "%s"' % which_display)

    def get_count(self, which_display, person=None):
        return self.get_items(which_display, person).count()

    def get_success_percent(self):
        return int((100.0 * self.success / (self.total - self.disabled)) if (self.total != 0) else 100)

    def get_absolute_url(self):
        return reverse('workflow:workflow_show', args=[self.pk, 'all'])


@receiver(pre_save, sender=Workflow)
def worklow_position_handler(sender, instance=None, **kwargs):
    if instance.position is None:
        last = Workflow.objects.filter(project=instance.project, archived=False).last()
        if last and last.position is not None:
            instance.position = last.position + 1
        else:
            instance.position = 0

def reset_workflow_items_count(workflow):
    items = workflow.get_items('all')
    d = {
        Item.VALIDATION_UNTESTED: 'untested',
        Item.VALIDATION_SUCCESS: 'success',
        Item.VALIDATION_FAILED: 'failed',
        Item.VALIDATION_DISABLED: 'disabled'
    }
    for k, v in d.items():
        setattr(workflow, v, 0)
    for item in items:
        setattr(workflow, d[item.validation], getattr(workflow,
            d[item.validation]) + 1)
    workflow.save()


def update_workflow_position(item, related_item=None):
    if related_item is not None:
        item.position = related_item.position
        Workflow.objects.filter(
                project=item.project,
                archived=False)\
            .update(position=F('position') + 1)
    else:
        related_item = Workflow.objects.filter(project=item.project,
                                               archived=False)\
                                       .last()
        item.position = related_item.position + 1 if related_item else 0
    item.save()


class Item(models.Model):
    VALIDATION_UNTESTED = 0
    VALIDATION_SUCCESS = 1
    VALIDATION_FAILED = 2
    VALIDATION_DISABLED = 3

    VALIDATION_CHOICES = (
        (VALIDATION_UNTESTED, _('Untested')),  # default
        (VALIDATION_SUCCESS, _('Success')),
        (VALIDATION_FAILED, _('Failed')),
        (VALIDATION_DISABLED, _('Disabled'))
    )

    item_model = models.ForeignKey(ItemModel, verbose_name=_('Item model'))
    name = models.CharField(null=True, blank=True, max_length=255)
    workflow = models.ForeignKey(Workflow, verbose_name=_('Workflow'))
    category = models.ForeignKey(ItemCategory, null=True, blank=True, verbose_name=_('Category'))
    assigned_to = models.ForeignKey(Person, null=True, blank=True, verbose_name=_('Assigned to'))
    assigned_to_name_cache = models.CharField(null=True, blank=True, max_length=50)
    validation = models.SmallIntegerField(
        choices=VALIDATION_CHOICES,
        default=0,
        verbose_name=_('Validation'),
    )
    updated_at = models.DateTimeField(null=True, editable=False)
    created_at = models.DateTimeField(null=True, editable=False)
    position = models.IntegerField(null=True, editable=False)
    comments_count = models.IntegerField(null=True, editable=False)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return '%s' % (self.item_model)

    def save(self, *args, **kwargs):
        if self.category is None:
            self.category = self.item_model.category
        if self.position is None:
            last_item = Item.objects.filter(workflow=self.workflow).order_by('position').last()
            if last_item is not None and last_item.position is not None:
                self.position = last_item.position + 1
            else:
                self.position = 0
        if self.name is None:
            self.name = self.item_model.name
        super(Item, self).save(*args, **kwargs)


@receiver(pre_save, sender=Item)
def updated_at_handler(sender, instance=None, **kwargs):
    instance.updated_at = timezone.now()


@receiver(pre_save, sender=Changelog)
@receiver(pre_save, sender=Item)
def created_at_handler(sender, instance=None, **kwargs):
    if instance.created_at is None:
        instance.created_at = timezone.now()
        if hasattr(instance, 'workflow'):
            instance.workflow.total += 1
            instance.workflow.save()


@receiver(post_delete, sender=Item)
def delete_item_handler(sender, instance=None, **kwargs):
    instance.workflow.total -= 1
    instance.workflow.save()

@receiver(pre_save, sender=Item)
def workflow_counts_handler(sender, instance=None, **kwargs):
    if instance.pk is not None:
        # On item update validation
        item = Item.objects.get(pk=instance.pk)
        workflow = item.workflow
        if item.validation != instance.validation:
            d = {
                Item.VALIDATION_UNTESTED: 'untested',
                Item.VALIDATION_SUCCESS: 'success',
                Item.VALIDATION_FAILED: 'failed',
                Item.VALIDATION_DISABLED: 'disabled'
            }
            attr = d[item.validation]
            if getattr(workflow, attr) > 0:
                setattr(workflow, attr, getattr(workflow, attr) - 1)
            attr = d[instance.validation]
            setattr(workflow, attr, getattr(workflow, attr) + 1)
    else:
        # On item creation
        workflow = instance.workflow
        attr = 'untested'
        setattr(workflow, attr, getattr(workflow, attr) + 1)
    workflow.save()

@receiver(post_delete, sender=Item)
def workflow_counts_delete_items(sender, instance=None, **kwargs):
    workflow = instance.workflow
    d = {
        Item.VALIDATION_UNTESTED: 'untested',
        Item.VALIDATION_SUCCESS: 'success',
        Item.VALIDATION_FAILED: 'failed',
        Item.VALIDATION_DISABLED: 'disabled'
    }
    attr = d[instance.validation]
    setattr(workflow, attr, getattr(workflow, attr) - 1)
    workflow.save()

def update_item_position(item, related_item=None):
    if related_item is not None:
        item.position = related_item.position
        Item.objects.filter(
                workflow=related_item.workflow,
                item_model__category=related_item.item_model.category,
                position__gte=related_item.position)\
            .update(position=F('position') + 1)
    else:
        related_item = Item.objects.filter(workflow=item.workflow,
                                           item_model__category=item.item_model.category)\
                                    .order_by('position')\
                                    .last()
        item.position = related_item.position + 1 if related_item else 0
    item.save()


class Comment(models.Model):
    item = models.ForeignKey(Item, verbose_name=_('Item'))
    person = models.ForeignKey(Person, verbose_name=_('Person'))
    date = models.DateTimeField(default=timezone.now, verbose_name=_('Date'))
    text = models.TextField(max_length=1000, verbose_name=_('Text'))

    def __unicode__(self):
        return '%s' % (self.text)


@receiver(post_save, sender=Comment)
def comments_count_save_handler(sender, instance=None, **kwargs):
    item = instance.item
    if item.comments_count is not None:
        Item.objects.filter(id=item.id).update(comments_count=F('comments_count') + 1)
    else:
        Item.objects.filter(id=item.id).update(comments_count = 1)


@receiver(post_delete, sender=Comment)
def comments_count_delete_handler(sender, instance=None, **kwargs):
    item = instance.item
    if item.comments_count - 1 < 0:
        Item.objects.filter(id=item.id).update(comments_count = 0)
    else:
        Item.objects.filter(id=item.id).update(comments_count = F('comments_count') - 1)
