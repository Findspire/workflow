#!/usr/bin/python
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
        for c in w.categories.all():
            for i, item in enumerate(Item.objects.filter(item_model__category=c, workflow=w)):
                item.position = i+1
                item.save()