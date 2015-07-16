#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013 Findspire

from django.http import HttpResponse, HttpResponseRedirect

import findspire.models
from findspire.utils.utils import request_test_decorator


def soft_authorize(request=None, model=None, collection_uuid=None, media_uuid=None,
                   profile_uuid=None, user=None):
    """Check if the user making that request is authorized to modify the model."""
    if user is None and request is not None:
        user = getattr(request, "user", None)

    if user is None or not user.is_authenticated():
        return False
    elif user.is_staff:
        return True

    # Get a list of all owned/delegated profiles
    user_profiles = []
    for profiles in user.get("profiles", {}).itervalues():
        user_profiles.extend(profiles)

    for user_profile in findspire.models.Profile.multiget(user_profiles).itervalues():
        if not user_profile:
            continue
        for subprofile_uuids in user_profile.get("profiles", {}).itervalues():
            user_profiles.extend(subprofile_uuids)

    def nested_check(submodel):
        if submodel is None:
            return False
        if type(submodel) is findspire.models.Profile and submodel.uuid in user_profiles:
            return True
        if "parent_media_uuid" in submodel:
            parent_media = findspire.models.Media.get(submodel["parent_media_uuid"])
            if nested_check(parent_media):
                return True
        if "parent_profile_uuid" in submodel:
            if submodel["parent_profile_uuid"] in user_profiles:
                return True
            else:
                parent_profile = findspire.models.Profile.get(submodel["parent_profile_uuid"])
                return nested_check(parent_profile)
        return False

    if type(model) is findspire.models.Media or type(model) is findspire.models.Profile or type(model) is findspire.models.Playlist:
        return nested_check(model)
    if type(model) is findspire.models.Moodboard:
        return model["parent_profile_uuid"] in user_profiles
    if type(model) is findspire.models.Collection:
        return model["profile_uuid"] in user_profiles
    if collection_uuid is not None:
        collection = findspire.models.Collection.get(collection_uuid)
        return collection["profile_uuid"] in user_profiles
    if media_uuid is not None:
        media = findspire.models.Media.get(media_uuid)
        return nested_check(media)
    if profile_uuid is not None:
        return profile_uuid in user_profiles

    return False


def with_acl(key, value, rejection=lambda x: HttpResponse(status=403)):
    """Authentification decorator.
    Ensure that request.user satisfy user[key] = value.
    example :

    @with_acl("backoffice", True)
    def MyBackOfficeView():
        ...
    """
    def _ensure_field(func):
        def test(request):
            if not request.user.is_authenticated():
                return False
            if request.user.get("is_staff", False):
                return True
            return 'acls' in request.user.all() \
                   and key in request.user.all()['acls'] \
                   and request.user.all()['acls'][key] == value
        return request_test_decorator(func, test, rejection)
    return _ensure_field


def backoffice_acl_required(func):
    """A shortcut - check acls for backoffice."""
    return with_acl("backoffice", True, rejection=lambda x: HttpResponseRedirect("/backoffice/login/"))(func)
