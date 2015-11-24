#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import django
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workflow.settings")
django.setup()

from workflow.apps.workflow.models import Item, ItemCategory, Workflow


def item_category():
    for item in Item.objects.all():
        if item.category is None:
            item.category = item.item_model.category
        if item.name is None:
            item.name = item.item_model.name
        item.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set item category and item name')
    parser.parse_args()
    if len(sys.argv) == 1:
        item_category()
