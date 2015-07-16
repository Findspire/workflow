# -*- coding: utf-8 -*-
# Copyright 2014 Findspire

"""File part of Findspire frontend project, providing template renderers."""

import django.template.response
from django.utils.cache import patch_cache_control
from django.http import HttpResponseRedirect


class TemplateResponse(django.template.response.TemplateResponse):
    def __init__(self, request, template, dic, cache_control_patch=None, **kwds):
        super(TemplateResponse, self).__init__(request, template, dic, **kwds)
        if cache_control_patch:
            patch_cache_control(self, **cache_control_patch)


class FrontendResponse(TemplateResponse):
    def __init__(self, request, template, dic, **kwds):
        # Patch the template path depending of the current site (desktop or mobile)
        is_mobile = request.is_mobile
        template = ("mobile" if is_mobile else "frontend") + "/" + template
        if 'base' in dic:
            dic['base'] = ("mobile" if is_mobile else "frontend") + "/" + dic['base']

        super(FrontendResponse, self).__init__(request, template, dic, **kwds)


class NativeAppRedirect(HttpResponseRedirect):
    """Implements HttpResponse with 'invalid' http scheme.
    By default and due to security reasons, custom url schemes are not allowed in django.
    (see https://www.djangoproject.com/weblog/2012/jul/30/security-releases-issued/)
    This subclass allow to redirect to a 'fs://*' url."""
    allowed_schemes = ["fs"]
