#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013 Findspire

"""Logging handler of the Findspire front project."""

from __future__ import absolute_import

import logging
import os.path
import traceback

import redis
import xtraceback

class RedisHandler(logging.Handler):
    """Redis log handler, best used with the logstash formatter"""
    def __init__(self, level=0, host='localhost', port=6379, db=0, log_key='log_key', defaults=None):
        logging.Handler.__init__(self, level=level)
        self._redis = None
        self._redis_host = host
        self._redis_port = port
        self._redis_db = db
        self._redis_log_key = log_key
        self._defaults = defaults if defaults is not None else {}

    def handle(self, record):
        try:
            if self._redis is None:
                self._redis = redis.StrictRedis(host=self._redis_host, port=self._redis_port, db=self._redis_db)
            for key, name in self._defaults.iteritems():
                setattr(record, key, name)

            if hasattr(record, "exc_info") and record.exc_info is not None:
                record.exc_message = traceback.format_exception_only(record.exc_info[0], record.exc_info[1])[-1].strip()

                # Extract more useful informations about the traceback
                tb_list = traceback.extract_tb(record.exc_info[2])
                exc_filename, exc_lineno, exc_function, _ = tb_list[-1]

                # Use a relative path for the filename
                exc_filename = os.path.relpath(exc_filename, os.path.dirname(__file__))

                record.exc_filename = exc_filename
                record.exc_lineno = exc_lineno
                record.exc_function = exc_function

            # Better formatting of exceptions
            try:
                with xtraceback.compat:
                    record.exc_text = None
                    msg = self.format(record)
            except:
                # Sometimes xtraceback fails fails, especially in Celery
                record.exc_text = None
                msg = self.format(record)

            self._redis.lpush(self._redis_log_key, msg)
        except:
            # Something went wrong: reset the Redis connection, just in case...
            self._redis = None
