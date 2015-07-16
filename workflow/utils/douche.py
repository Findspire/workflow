#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Findspire

"""File part of Findspire frontend project, used to provide a helper to avoid
document update conflicts in CouchDB."""

import random
import time

import redis
import redis_lock

from findspire import settings
import findspire.models

class DoucheError(Exception):
    def __init__(self, msg, history=None):
        super(DoucheError, self).__init__(msg)
        self._history = history

    def __str__(self):
        res = super(DoucheError, self).__str__()
        if self._history is not None:
            res += "\nHistory: "
            res += "\n- ".join(self._history)
        return res

class Douche(object):
    """DOcument Update Conflict Handler for Everyone"""
    test_instances = []

    def __init__(self, retries=8, min_retry_delay=0.2, max_retry_delay=0.5):
        """Initialize the DOUCHE"""
        self.retries = retries
        self.min_retry_delay = min_retry_delay
        self.max_retry_delay = max_retry_delay
        self.models = set()
        self.tasks = []
        self.history = []
        self.notifications = {}

        self.tries = 0
        self._saved = False
        self._use_bulk_update = False

        host, port, db = settings.DLM_CONFIG
        self.dlm = redis.StrictRedis(host, port, db)

    @property
    def saved(self):
        """Indicates whether all the data added to the douche were successfully saved"""
        return self._saved

    def add(self, *models):
        """Add a few models to the DOUCHE

        Once save_all is called, all these models will be saved atomically."""
        if self._saved:
            raise DoucheError("Tried to add models after save")
        self.models.update(models)
        self.history.append("add: " + ", ".join([repr(model) for model in models]))

    def delay(self, *tasks):
        """Add a few tasks to the DOUCHE

        When save_all() is successful, all these tasks will be started with `.delay()`."""
        if self._saved:
            raise DoucheError("Tried to add tasks after save")
        self.tasks.extend(tasks)
        self.history.append("add_task: " + ", ".join([repr(task) for task in tasks]))

    def notify(self, parent_profile_uuid, *notifications):
        """Add notifications to the DOUCHE

        Notifications must have been added with `.add()` first."""
        if self._saved:
            raise DoucheError("Tried to add notifications after save")
        if not all([notif in self.models for notif in notifications]):
            raise DoucheError("Notification was not added first")
        self.notifications.setdefault(parent_profile_uuid, set())
        self.notifications[parent_profile_uuid].update(set(notifications))

    def enable_bulk_update__yes_I_know_what_I_am_doing(self, reason):
        """Enable bulk update. You probably don't want to do that."""
        if reason == "I like to live dangerously":
            self._use_bulk_update = True
        else:
            raise ValueError("No valid reason to use a bulk update")

    def save_all(self):
        """Save all the added models at once and return `True' if it succeeded."""
        if self._saved:
            raise DoucheError("Douche already saved")

        if settings.TEST_MODE:
            self._saved = True
            self.test_instances.append(self)
            return True

        if self._try_save_all():
            self._saved = True
            for parent_profile_uuid, notifications in self.notifications.iteritems():
                notifs = findspire.models.Notifications(parent_profile_uuid)
                for notif in notifications:
                    notifs.add(notif)
            for task in self.tasks:
                task.delay()
            return True

        else:
            self.tries += 1
            if self.tries >= self.retries:
                raise DoucheError("Too many retries", self.history)

            retry_delay = random.uniform(self.min_retry_delay, self.max_retry_delay)
            self.history.append("retry %d: %.3f s" % (self.tries, retry_delay))
            time.sleep(retry_delay)
            self._reload_all()
            self.models.clear()
            self.tasks = []
            self.notifications.clear()
            return False

    def _try_save_all(self):
        """Try to acquire locks for all the models, then to check if they can be saved,
        and then to save them."""
        locks = []
        all_uuids = {}

        try:
            # We need to get locks for all the models. But we want to avoid
            # deadlocks! To do so, we use a short-lived "master lock" that is only
            # used to acquire the other locks.
            master_lock = redis_lock.Lock(self.dlm, "dlm:master", expire=settings.DLM_EXPIRE)
            with master_lock:
                # Try to get locks for all models. They will be released in the
                # finally clause, so it's safe to exit from this function without
                # triggering a deadlock.
                for model in self.models:
                    lock_name = "dlm:%s:%s" % (model.name, model.uuid)
                    lock = redis_lock.Lock(self.dlm, lock_name, expire=settings.DLM_EXPIRE)

                    if lock.acquire(blocking=False):
                        locks.append(lock)
                        self.history.append("lock acquired: " + repr(model))

                        cls = type(model)
                        if cls not in all_uuids:
                            all_uuids[cls] = {}

                        all_uuids[cls][model.uuid] = model.get("_rev", None)

                    else:
                        self.history.append("lock NOT acquired: " + repr(model))
                        return False

            # Now check if the models were not updated "upstream" before trying
            # to save them.
            for cls, cls_data in all_uuids.iteritems():
                uuids = cls_data.keys()
                new_revs = cls.multihead(*uuids)
                if new_revs != cls_data:
                    self.history.append("revs mismatch: " + str(cls_data) + " vs " + str(new_revs))
                    return False

            # All the checks passed: now try to save everything...
            if self._use_bulk_update:
                # Oh my.
                # Group by model type
                by_type = {}
                for model in self.models:
                    model_cls = type(model)
                    by_type.setdefault(model_cls, [])
                    by_type[model_cls].append(model)

                # Do a bulk update for each type
                for model_cls, models in by_type.iteritems():
                    if len(models) > 0:
                        model_cls.bulk_save(*models)

            else:
                for model in self.models:
                    model.save()

            # And done! :)
            return True

        finally:
            for lock in locks:
                lock.release()

    def _reload_all(self):
        """Reload all the models managed by this DOUCHE."""
        # TODO: somehow use multigets.
        for model in self.models:
            model.reload()
