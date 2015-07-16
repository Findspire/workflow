#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright 2014 Findspire


class URN(object):
    """ Uniform resource name.

    >>> urn = URN.parse("urn:media:x123adsdfva")
    >>> urn.ns
    'media'
    >>> urn.id
    'x123adsdfva'
    >>> str(urn)
    'urn:media:x123adsdfva'

    >>> urn = URN(ns='playlist', id='foo')
    >>> urn.ns
    'playlist'
    >>> urn.id
    'foo'
    >>> str(urn)
    'urn:playlist:foo'
    """

    @classmethod
    def parse(cls, ref):
        """ Parse the string ref as a urn.

        Raises a ValueError is ref is not an urn.
        """
        ns, id = cls.split(ref)
        return cls(ns=ns, id=id)

    @classmethod
    def split(cls, ref):
        """ Split the components and return (ns, id) tuple.
        """
        if not URN.isURN(ref):
            raise ValueError("{} is not an urn.".format(ref))
        _nop, ns, id = ref.split(":", 3)
        return ns, id

    @staticmethod
    def isURN(ref):
        """ Tell whether ref is an urn.
        """
        return ref.startswith("urn:")

    def __init__(self, ref=None, ns=None, id=None, obj=None):
        """ if ref is a urn, parses it, else use ns and id parameters.
        """
        if obj is not None:
            self.ns, self.id = obj.name, obj.uuid
        elif ref is not None:
            self.ns, self.id = self.split(ref)
        elif ns is not None:
            self.ns = ns
            self.id = id

    def __str__(self):
        return "urn:%s:%s" % (self.ns, self.id)

    def __eq__(self, other):
        return str(other) == str(self)


class CompatURN(URN):
    """ Preserve compatibility where it did not use an urn.

    >>> media_uuid = CompatURN("media", "23afxcvasdfasdf")
    >>> media_urn  = CompatURN("media", "urn:media:adsfadsfadsf")
    >>> playlist_urn = CompatURN("media", "urn:playlist:xczvvasdf")
    >>> str(media_uuid)
    '23afxcvasdfasdf'
    >>> str(playlist_urn)
    'urn:playlist:xczvvasdf'
    >>> str(media_urn)
    'adsfadsfadsf'
    """

    def __init__(self, ns_default, ref):
        self.ns_default = ns_default
        if URN.isURN(ref):
            super(CompatURN, self).__init__(ref)
        else:
            super(CompatURN, self).__init__(ns=ns_default, id=ref)

    def __str__(self):
        if self.ns_default == self.ns:
            return str(self.id)
        return super(CompatURN, self).__str__()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
