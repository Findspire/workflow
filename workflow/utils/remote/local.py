#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright 2013 Findspire

from base import Backend
import os

class Local(Backend):
    def __init__(self, credentials):
        super(Local, self).__init__(credentials)
        if 'rootdir' not in credentials:
            raise Backend.ConfigError("rootdir not specified on credentials")
        self.local_dir = os.path.join(self.credentials['rootdir'], self.credentials['basedir'])

    def connect(self):
        if not os.path.isdir(self.local_dir):
            raise Backend.BackendError("'%s' is not a directory" % self.local_dir)

    def listdir(self, directory):
        return os.listdir(os.path.join(self.local_dir, directory))

    def download(self, path):
        filepath = os.path.join(self.local_dir, path)
        return { "filepath": filepath, "filep": open(filepath) }
