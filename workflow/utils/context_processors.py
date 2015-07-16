#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Findspire

"""File part of Findspire frontend project, used to provide new global variables
in Django templates."""

def magic(request):
    """Add useful global variables to Django template contexts.

    The name of this function sucks, but I don't have any better idea :)"""
    ret = {}

    # Facebook OpenGraph crawler user agent
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    if not isinstance(user_agent, basestring):
        user_agent = ""
    ret["is_facebook_crawler"] = user_agent.startswith("facebookexternalhit/")

    return ret
