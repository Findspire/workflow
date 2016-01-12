#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import django
import sys
import argparse

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH)
django.setup()


from workflow.apps.workflow.models import Workflow, ItemCategory


def assign_category_position():
    for w in Workflow.objects.all():
        for i, c in enumerate(w.categories.all()):
            c.position = i
            c.save()
            print('%s position = %d' % (c.name, i))
    print('Done - Update successfull')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Assign position of workflow categories')
    parser.parse_args()
    if len(sys.argv) == 1:
        assign_category_position()