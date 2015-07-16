#!/usr/bin/env python

import optparse
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'findspire.settings'
from django.contrib.auth.models import User

parser = optparse.OptionParser()
parser.add_option("--status", dest='status', default=False, action='store_true', help="Return superuser status")
(opts, args) = parser.parse_args()

if opts.status:
    try:
        root = User.objects.get(username__exact='root')
        if root.is_superuser and root.is_staff and root.is_active:
            print "Superuser is configured correctly"
            sys.exit(0)
        else:
            print "User \"root\" is not configured"
            sys.exit(2)
    except Exception, e:
        print "Superuser does not exist"
        sys.exit(1)


try:
    root = User.objects.get(username__exact='root')
    root.is_superuser = True
    root.is_staff = True
    root.is_active = True
except User.DoesNotExist:
    # TODO : Security...
    root = User.objects.create_user('root', 'a@a.com', 'a')
    root.is_superuser = True
    root.is_staff = True
    root.is_active = True
root.save()
