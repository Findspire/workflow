#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015 Findspire


""" This module contains utility functions to help ES query construction.
"""

from pyelasticsearch.client import es_kwargs
from findspire.utils.utils import traverse


def add_sort(container, sort, desc=True):
    """ Add sort parameter to container (query dict).

    :param sort: can be a list, a dict or a string.
    :param desc: indicate the order (descending or ascending).
                 It is used only if sort is a string.
    """
    if isinstance(sort, (list, dict)):
        container['sort'] = sort
    elif isinstance(sort, basestring):
        container['sort'] = {sort: {"order": desc and "desc" or "asc"}}
    return container

def addafter(container, keys, values, desc=True):
    """ Add an after parameter to the given container.

    :param container: The container in which append the ES options.
    :param keys: A list of field names or a list of dicts with field name as key (because used by
    MetadataInterface.find_references()).
    :param values: A list of values for each key.
    """
    # FIXME: enable _cache in "or" and "and" filters?
    def cmp_null(key):
        if type(key) is dict:
            key = key.keys()[0]
        return {"missing": {"field": key, "existence": True, "null_value": True}}

    def cmp_lt(key, value):
        if type(key) is dict:
            key = key.keys()[0]
        return {"range": {key: {"lt" if desc else "gt": value}}}

    def cmp_eq(key, value):
        if type(key) is dict:
            key = key.keys()[0]
        if value is None:
            return cmp_null(key)
        else:
            return {"term": {key: value}}

    def make_range(keys, values):
        if len(keys) == 1:
            key, value = keys[0], values[0]
            if value is None:
                return cmp_null(key)
            else:
                return {
                    "or": [
                        cmp_lt(key, value),
                        cmp_null(key)
                    ]
                }
        else:  # len(keys) > 1
            return {
                "or": [
                    cmp_lt(keys[0], values[0]),
                    cmp_null(keys[0]),
                    {
                        "and": [
                            cmp_eq(keys[0], values[0]),
                            make_range(keys[1:], values[1:])
                        ]
                    }
                ]
            }

    if len(keys) != len(values):
        raise ValueError("Incompatible sizes for keys and values")
    if len(keys) > 0:
        container.append(make_range(keys, values))


@es_kwargs('scroll')
def _elasticsearch_scroll(es, scroll_id, query_params):
    return es.send_request('GET', ['_search', 'scroll'], scroll_id, query_params, encode_body=False)


def elasticsearch_scan(es, query, index, doc_type, es_scroll='1m', **kwargs):
    """Search with scan/scroll provides efficient scanning for huge results queries.

    It is less stessfull for ES than relying on sort for paging results.
    """
    # import pprint
    scan = es.search(query, index=index, doc_type=doc_type, es_search_type='scan', es_scroll=es_scroll, **kwargs)
    _scroll_id = scan.get('_scroll_id')
    while _scroll_id:
        scan = _elasticsearch_scroll(es, scan['_scroll_id'], es_scroll=es_scroll)
        if scan['timed_out']:
            raise RuntimeError("ES cursor timed out.")
        _scroll_id = scan.get('_scroll_id')
        hits = traverse(scan, ("hits", "hits"), [])
        if not hits:
            raise StopIteration
        for h in hits:
            yield h
