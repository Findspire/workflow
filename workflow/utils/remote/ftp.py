#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright 2013 Findspire

from base import Backend

class FTP(Backend):
    def __init__(self, credentials):
        super(FTP, self).__init__(credentials)
