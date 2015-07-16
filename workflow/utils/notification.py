#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Findspire

"""File part of Findspire frontend project, used to prepare user notifications"""

import datetime
import json

import dateutil.parser
import redis
import redis_lock

from findspire import settings
import findspire.apps.tasks.mail as mail
from findspire.models import User


def authorize(request):
    """Ensure that the current user can trigger a notification."""
    if settings.DEBUG:
        return True
    if not hasattr(request, "user") or not request.user.is_authenticated():
        # Anonymous users can't send notifications
        return False

    # Staff can't send notifications either
    return not request.user.is_staff


def rate_limited_mail(limit_delta, mail_type, user_uuid, template_ctx):
    """Send a notification mail, with rate limiting.

    :param limit_delta: A `datetime.timedalta` object specifying the interval between 2 mails.
    :param mail_type: Type of the mail to send.
    :param user_uuid: User to whom the mail will be sent.
    :param template_ctx: Mail template context.
    """

    now = datetime.datetime.utcnow()
    red = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB["notif"])

    # Get a lock so we're safe
    lock_key = "notif:%s:%s:lock" % (mail_type, user_uuid)
    with redis_lock.Lock(red, lock_key):
        # Add the mail parameters to a list that is specific to the mail type and
        # target user. This way we can easily aggregate several notifications in a
        # single mail.
        ctx_key = "notif:%s:%s:contexts" % (mail_type, user_uuid)
        red.rpush(ctx_key, json.dumps(template_ctx))

        # In Redis, we store the last time a mail was sent, a flag indicating if
        # another mail sending task is already scheduled.
        last_key = "notif:%s:%s:last_mail_time" % (mail_type, user_uuid)
        next_key = "notif:%s:%s:next_mail_scheduled" % (mail_type, user_uuid)
        last_val, next_val = red.mget(last_key, next_key)
        last_mail_time = dateutil.parser.parse(last_val) if last_val else None
        next_scheduled = (next_val == "true")

        if next_scheduled:
            # If another mail is already scheduled, there's nothing left to do.
            return

        if last_mail_time is None or last_mail_time + limit_delta <= now:
            # If the previous mail is old enough, we can send the mail right now
            red.set(last_key, now.isoformat(), ex=int(limit_delta.total_seconds()))
            mail.send_notification.delay(mail_type, user_uuid)

        else:
            # The last mail is not old enough, but we can schedule the next one.
            eta = last_mail_time + limit_delta
            red.set(next_key, "true", ex=int(limit_delta.total_seconds()))
            mail.send_notification.apply_async((mail_type, user_uuid), eta=eta)


def mail_inspired(request, inspired_profile, by_profile):
    """Notify a user that one of his profile has been inspired"""
    if not authorize(request):
        return

    inspired_user = User.get(inspired_profile["parent_user_uuid"])

    # Only send the notification if the inspiring profile is a page, or a passionate
    if not inspired_user or inspired_profile["type"] not in ("page", "passionate"):
        return

    dic = {
        "inspired_profile_uuid": inspired_profile.uuid,
        "by_profile_uuid": by_profile.uuid,
    }

    rate_limited_mail(datetime.timedelta(hours=24), "inspired_profile", inspired_user.uuid, dic)


def new_user(newuser):
    """Notify the staff that a new user account was created."""

    mail.send_new_user_notification.delay(newuser.uuid, settings.NEWUSERS_NOTIF_MAIL)


def new_profile(newprofile):
    """Notify the staff that a new profile has been created.
    """
    parent_profile_uuid = newprofile.get('parent_profile_uuid', None)
    if not parent_profile_uuid:
        parent_profile_uuid = User.get(newprofile['parent_user_uuid'])['main_profile_uuid']
    mail.send_new_profile_notification.delay(newprofile.uuid, parent_profile_uuid,
                                             settings.NEWUSERS_NOTIF_MAIL)
