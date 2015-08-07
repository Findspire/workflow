#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Each Person has a set of Skills. Each Skill has a ForeignKey to a SkillSubject
(which has a name, a category and a description) and a strength. Multiple Person
can have the same SkillSubject with different strength (that's the purpose of
the Skill model).

"""

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


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

    user = models.OneToOneField(User)
    arrival_date = models.DateField()
    contract_type = models.SmallIntegerField(
        choices=CONTRACT_CHOICEs,
        default=0,
    )

    def __unicode__(self):
        return '%s' % (self.user)


class Team(models.Model):
    name = models.CharField(max_length=64)
    leader = models.ForeignKey(Person, related_name='leader')
    members = models.ManyToManyField(Person, related_name='members')

    def __unicode__(self):
        return '%s' % (self.name)


class SkillCategory(models.Model):
    class Meta:
        verbose_name = 'skill category'
        verbose_name_plural = 'skill categories'

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' % (self.name)


class SkillSubject(models.Model):
    class Meta:
        verbose_name = 'skill subject'
        verbose_name_plural = 'skill subjects'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(SkillCategory)
    description = models.CharField(max_length=1024, null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.category, self.name)


class Skill(models.Model):
    class Meta:
        verbose_name = 'skill instance'
        verbose_name_plural = 'skill instances'

    techno = models.ForeignKey(SkillSubject)
    person = models.ForeignKey(Person)
    strength = models.IntegerField()

    def __unicode__(self):
        return '%s - %s - %d' % (self.person, self.techno, self.strength)
