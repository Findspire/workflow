#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django
import argparse


PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workflow.settings")
sys.path.append(PATH)
django.setup()

from django.db.models import F
from workflow.apps.workflow.models import Item, Workflow, Comment


def set_comments_count():
    for w in Workflow.objects.all():
        for i in w.get_items('all'):
            for c in Comment.objects.filter(item=i):
                Item.objects.filter(id=c.id).update(comments_count = F('comments_count') + 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set comments_count field of items')
    parser.parse_args()
    if len(sys.argv) == 1:
        set_comments_count()
