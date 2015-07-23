#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import models as AuthModels
from django.db import models
from django.utils import timezone


class ContractType(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return '%s' % (self.name)


class Person(models.Model):
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    django_user = models.OneToOneField(AuthModels.User, null=True, blank=True)
    arrival_date = models.DateField()
    departure_date = models.DateField(null=True, blank=True)
    contract_type = models.ForeignKey(ContractType)
    access_card = models.CharField(max_length=64, null=True, blank=True)
    token_serial = models.CharField(max_length=32, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)

    def __unicode__(self):
        return '%s %s' % (self.firstname, self.lastname.upper())


class Team(models.Model):
    name = models.CharField(max_length=64)
    leader = models.ForeignKey(Person)

    def __unicode__(self):
        return '%s' % (self.name)

    def save(self, *args, **kwargs):
        super(Team, self).save(*args, **kwargs)
        tp = TeamPerson(team=self, person=self.leader)
        tp.save()


class TeamPerson(models.Model):
    person = models.ForeignKey(Person)
    team = models.ForeignKey(Team)

    def save(self, *args, **kwargs):
        super(TeamPerson, self).save(*args, **kwargs)
        categories = CompetencesSubjectCategory.objects.filter(part_of_team=self.team)
        for category in categories:
            competence_subjects = CompetencesSubject.objects.filter(competence_subject_category=category)
            for competence_subject in competence_subjects:
                new_comp = Competence(competence_subject_id=competence_subject.id, person=self.person)
                new_comp.save()

    def __unicode__(self):
        return '%s - %s' % (self.team, self.person)


class CompetencesSubjectCategory(models.Model):
    name = models.CharField(max_length=255)
    part_of_team = models.ForeignKey(Team)

    def __unicode__(self):
        return '%s' % (self.name)


class CompetencesSubject(models.Model):
    name = models.CharField(max_length=255)
    competence_subject_category = models.ForeignKey(CompetencesSubjectCategory)
    description = models.CharField(max_length=1024, null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.competence_subject_category, self.name)

    def save(self, *args, **kwargs):
        super(CompetencesSubject, self).save(*args, **kwargs)
        team_persons = TeamPerson.objects.filter(team=self.competence_subject_category.part_of_team)
        for team_person in team_persons:
            new_comp = Competence(person=team_person.person, competence_subject=self)
            new_comp.save()


class CompetencesType(models.Model):
    name = models.CharField(max_length=64)
    strength = models.IntegerField(null=False)

    def __unicode__(self):
        return '%s' % (self.name)


class Competence(models.Model):
    comptype = models.ForeignKey(CompetencesType, null=True, related_name='comptype')
    target_comptype = models.ForeignKey(CompetencesType, null=True)
    person = models.ForeignKey(Person)
    competence_subject = models.ForeignKey(CompetencesSubject)

    def __unicode__(self):
        return '%s - %s : %s -> %s' % (self.person, self.competence_subject, self.comptype, self.target_comptype)


class Workflow(models.Model):
    name = models.CharField(max_length=32)
    teams = models.ManyToManyField(Team)
    leaders = models.ManyToManyField(Person)

    def __unicode__(self):
        return '%s' % (self.name)


class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(Workflow)
    creation_date = models.DateField(null=False, auto_now=True)
    version = models.CharField(max_length=128)

    def __unicode__(self):
        return '%s - %s' % (self.workflow, self.version)


class WorkflowCategory(models.Model):
    workflow = models.ForeignKey(Workflow)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return '%s - %s' % (self.workflow, self.name)


class Item(models.Model):
    workflow_category = models.ForeignKey(WorkflowCategory)
    label = models.CharField(max_length=512)
    details = models.TextField(max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.workflow_category, self.label)


class Validation(models.Model):
    label = models.CharField(max_length=32)

    def __unicode__(self):
        return '%s' % (self.label)


class WorkflowInstanceItem(models.Model):
    workflowinstance = models.ForeignKey(WorkflowInstance)
    item = models.ForeignKey(Item)
    validation = models.ForeignKey(Validation, null=True)
    assigned_to = models.ForeignKey(Person, null=True, blank=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.workflowinstance, self.item.workflow_category.name, self.item.label)


class CommentInstanceItem(models.Model):
    item = models.ForeignKey(WorkflowInstanceItem)
    person = models.ForeignKey(Person, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    comments = models.TextField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.comments)
