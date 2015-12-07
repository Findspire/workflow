#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django
import argparse


PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH)
django.setup()


from workflow.apps.workflow.models import Item, ItemCategory, Workflow, Project


def workflow_position():
    for p in Project.objects.all():
        for i, w in enumerate(Workflow.objects.filter(project=p, archived=False)):
            w.position = i
            w.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set workflow position')
    parser.parse_args()
    if len(sys.argv) == 1:
        workflow_position()
