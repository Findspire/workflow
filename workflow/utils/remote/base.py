#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright 2013 Findspire

class Backend(object):
    class BackendError(Exception):
        def __init__(self, message):
            super(Backend.BackendError, self).__init__(message)

    class ConfigError(Exception):
        def __init__(self, message):
            super(Backend.ConfigError, self).__init__(message)

    def __init__(self, credentials):
        if 'basedir' not in credentials:
            raise Backend.ConfigError("basedir not specified on credentials")
        self.credentials = credentials

    def connect(self):
        raise NotImplemented

    def listdir(self, directory):
        raise NotImplemented

    def download(self, path):
        raise NotImplemented
