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


from workflow.apps.workflow.models import Item


def assigned_to_name():
    for i in Item.objects.all():
        if i.assigned_to is not None:
            i.assigned_to_name_cache = i.assigned_to.user.username
            i.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy item owner in assigned_to field top assigned_to_name_cache field')
    parser.parse_args()
    if len(sys.argv) == 1:
        assigned_to_name()