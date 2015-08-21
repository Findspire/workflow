#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2015 Findspire
#
# This file used to be part of Progdupeupl but the algo has been totally rewritten
# cf. https://bitbucket.org/MicroJoe/progdupeupl/src/62de1acc20f7673220deafa7464b2d8130a2841e/pdp/utils/paginator.py?at=master#cl-21
#

def paginator_range(current, stop, start=1):
    """Build a paginator.
    Ex : paginator_range(10, 20) returns [1, 2, None, 8, 9, 10, 11, 12, None, 19, 20]

    :param current: current page
    :param stop: last page
    :param start: first page

    :return: a list of page numbers for shown pages and None when pages are skipped
    """

    LIMIT = 2
    ret = []
    for i in range(start, stop+1):
        # if beginning or middle or end
        if (abs(start-1-i) <= LIMIT) or (abs(current-i) <= LIMIT) or (abs(stop+1-i) <= LIMIT):
            ret.append(i)
        # else : skip pages. Add None unless already added
        elif ret[-1] != None:
            ret.append(None)
    return ret
