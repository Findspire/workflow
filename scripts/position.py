#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django


PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH)
django.setup()


from workflow.apps.workflow.models import Item, ItemCategory, Workflow

if __name__ == "__main__":
    for w in Workflow.objects.all():
        for i, item in enumerate(w.get_items('all')):
            item.position = i
            item.save()
