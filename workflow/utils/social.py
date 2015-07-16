#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Findspire

"""File part of Findspire frontend project, used to handle social sharing links."""

import urllib

def get_twitter_link(language, link, text=None):
    """Create a link for sharing on Twitter"""
    data = {
        "url": link,
        "related": "Findspire",
        "via": "Findspire",
    }
    if text is not None:
        data["text"] = text.encode("utf-8")
    url = "https://twitter.com/share?" + urllib.urlencode(data)
    return url

def get_facebook_link(language, link):
    """Create a link for sharing on Facebook"""
    data = {"u": link}
    url = "https://www.facebook.com/sharer/sharer.php?" + urllib.urlencode(data)
    return url
