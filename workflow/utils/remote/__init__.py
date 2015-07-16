#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright 2013 Findspire

from .ftp import FTP
from .local import Local

def connect_remote(credentials):
    if credentials['type'] == 'ftp':
        ctx = FTP(credentials)
        ctx.connect()
        return ctx

    if credentials['type'] == 'local':
        ctx = Local(credentials)
        ctx.connect()
        return ctx
