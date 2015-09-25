#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire

"""

Each Person has a set of Skills. Each Skill has a ForeignKey to a SkillSubject
(which has a name, a category and a description) and a strength. Multiple Person
can have the same SkillSubject with different strength (that's the purpose of
the Skill model).

"""

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Person(models.Model):
    CONTRACT_CDI = 0
    CONTRACT_CDD = 1
    CONTRACT_STAGE = 3
    CONTRACT_FREELANCE = 4

    CONTRACT_CHOICEs = (
        (CONTRACT_CDI, _('Permanent contract')),  # default
        (CONTRACT_CDD, _('Fixed-term contract')),
        (CONTRACT_STAGE, _('Internship')),
        (CONTRACT_FREELANCE, _('Freelance')),
    )

    user = models.OneToOneField(User, verbose_name=_('User'))
    arrival_date = models.DateField(verbose_name=_('Arrival date'))
    contract_type = models.SmallIntegerField(
        choices=CONTRACT_CHOICEs,
        default=0,
        verbose_name=_('Contract'),
    )

    def __unicode__(self):
        return '%s' % (self.user)


class Team(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    leader = models.ForeignKey(Person, related_name='leader', verbose_name=_('Leader'))
    members = models.ManyToManyField(Person, related_name='members', verbose_name=_('Members'))

    def __unicode__(self):
        return '%s' % (self.name)


class SkillCategory(models.Model):
    class Meta:
        verbose_name = _('Skill category')
        verbose_name_plural = _('Skill categories')

    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __unicode__(self):
        return '%s' % (self.name)


class SkillSubject(models.Model):
    class Meta:
        verbose_name = _('Skill subject')
        verbose_name_plural = _('Skill subjects')

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    category = models.ForeignKey(SkillCategory, verbose_name=_('Category'))
    description = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_('Description'))

    def __unicode__(self):
        return '%s - %s' % (self.category, self.name)


class Skill(models.Model):
    class Meta:
        verbose_name = _('Skill instance')
        verbose_name_plural = _('Skill instances')

    techno = models.ForeignKey(SkillSubject, verbose_name=_('Skill subject'))
    person = models.ForeignKey(Person, verbose_name=_('Person'))
    strength = models.IntegerField(verbose_name=_('Strength'))

    def __unicode__(self):
        return '%s - %s - %d' % (self.person, self.techno, self.strength)
