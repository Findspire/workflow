#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django
import argparse


PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH)
django.setup()

from workflow.apps.workflow.models import Workflow, Item


def set_counts_items():
    for w in Workflow.objects.all():
        print('Update : %s' % w)
        w.success = 0
        w.failed = 0
        w.untested = 0
        w.disabled = 0
        w.total = 0
        for i in w.get_items('all'):
            d = {
                Item.VALIDATION_UNTESTED: 'untested',
                Item.VALIDATION_SUCCESS: 'success',
                Item.VALIDATION_FAILED: 'failed',
                Item.VALIDATION_DISABLED: 'disabled'
            }[i.validation]
            setattr(w, d, getattr(w, d) + 1)
        w.total = Item.objects.filter(workflow=w, category__in=w.categories.all()).count()
        w.save()
    print('Done - Successfull updated !')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set counts items attr of workflow')
    parser.parse_args()
    if len(sys.argv) == 1:
        set_counts_items()