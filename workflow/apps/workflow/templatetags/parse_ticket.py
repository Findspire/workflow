#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from django.template import Library
from django.conf import settings

register = Library()


@register.filter
def get_tickets(value):
    tickets_id = re.findall(r'#([\d]+)', value)
    return [(settings.BUG_TRACKER_URL + ticket_id, ticket_id) for ticket_id in tickets_id]
