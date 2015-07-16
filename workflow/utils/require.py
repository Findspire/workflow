# -*- coding: utf-8 -*-
# Copyright 2014 Findspire

"""Require data files and integrate them with the Django auto-reloader"""

import hashlib
import os.path
import sys

class _pseudomodule(object):
    def __init__(self, file_name):
        self.__file__ = file_name

_cache = {}

def require(file_name):
    path = os.path.join(os.path.dirname(__file__), "..", "..", file_name)
    path = os.path.abspath(path)

    if path in _cache:
        return _cache[path]

    with open(path) as inp:
        data = inp.read()
    _cache[path] = data

    path_md5 = hashlib.md5()
    path_md5.update(path)
    path_md5 = path_md5.hexdigest()
    module_name = "_findspire_require_ " + path_md5
    sys.modules[module_name] = _pseudomodule(path)

    return data
