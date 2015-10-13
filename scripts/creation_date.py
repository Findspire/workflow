#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import django
import datetime
from django.utils import timezone

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workflow.production_settings")
django.setup()


from workflow.apps.workflow.models import Item

start_date = timezone.now() - datetime.timedelta(weeks=4) # Select the start date
time_delta = datetime.timedelta(seconds=1) # Select the delta time between item
items_list = [item for item in Item.objects.all().order_by('-pk')] # Retrieve all items objects ordered by pk


for item in items_list:
    if not item.created_at:
        item.created_at = start_date
        item.save()
        start_date += time_delta
