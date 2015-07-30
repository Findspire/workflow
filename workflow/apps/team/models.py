#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class ContractType(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return '%s' % (self.name)


class Person(models.Model):
    user = models.OneToOneField(User)
    arrival_date = models.DateField()
    departure_date = models.DateField(null=True, blank=True)
    contract_type = models.ForeignKey(ContractType)
    access_card = models.CharField(max_length=64, null=True, blank=True)
    token_serial = models.CharField(max_length=32, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.user)


class Team(models.Model):
    name = models.CharField(max_length=64)
    leader = models.ForeignKey(Person, related_name='leader')
    members = models.ManyToManyField(Person, related_name='members')

    def __unicode__(self):
        return '%s' % (self.name)


class CompetenceCategory(models.Model):
    class Meta:
        verbose_name = 'competence category'
        verbose_name_plural = 'competence categories'

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' % (self.name)


class CompetenceSubject(models.Model):
    class Meta:
        verbose_name = 'competence subject'
        verbose_name_plural = 'competence subjects'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(CompetenceCategory)
    description = models.CharField(max_length=1024, null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.category, self.name)


class CompetenceInstance(models.Model):
    class Meta:
        verbose_name = 'competence instance'
        verbose_name_plural = 'competence instances'

    techno = models.ForeignKey(CompetenceSubject)
    person = models.ForeignKey(Person)
    strength = models.IntegerField()
    # status : want to use or not

    def __unicode__(self):
        return '%s - %s - %d' % (self.person, self.techno, self.strength)
