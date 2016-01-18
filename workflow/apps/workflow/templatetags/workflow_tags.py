#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire

import re
from django.template import Library
from django.conf import settings
from workflow.apps.workflow.models import Item

register = Library()


@register.filter
def get_tickets(value):
    tickets_id = re.findall(r'#([\d]+)', value)
    return [(settings.BUG_TRACKER_URL + ticket_id, ticket_id) for ticket_id in tickets_id]


@register.filter
def get_count(workflow, param):
    return workflow.get_count(param)


@register.filter
def percent(workflow, value):
    value_percent = (getattr(workflow, value) * 100.0) / workflow.total if workflow.total != 0 else 100
    return round(value_percent, 3)


@register.filter
def to_dot(value):
    if not isinstance(value, str):
        value = str(value)
    return value.replace(',', '.')


@register.filter
def get_status(item):
    if item.validation == Item.VALIDATION_SUCCESS:
        return 'success'
    elif item.validation == Item.VALIDATION_UNTESTED:
        return 'untested'
    elif item.validation == Item.VALIDATION_FAILED:
        return 'failed'

    elif item.validation == Item.VALIDATION_DISABLED:
        return 'disabled'


@register.filter
def u(s):
    if isinstance(s, unicode):
        return s.encode('utf-8', errors='ignore')
    return s
