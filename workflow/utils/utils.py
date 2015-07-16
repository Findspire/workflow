# -*- coding: utf-8 -*-
# Copyright 2014 Findspire

''' File part of Findspire frontend project,
    used to store utils functions '''

import base64
import copy
from datetime import datetime
import encodings.idna
import functools
from hashlib import md5, sha512
import hmac
import inspect
import json
import os
import os.path
import re
import subprocess
import tempfile
import time
import types
import unicodedata
import unidecode
from findspire.middleware import get_current_request

if __name__ == "__main__":
    # Used for doctests
    import sys
    os.environ['DJANGO_SETTINGS_MODULE'] = 'findspire.settings'
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import slugify as py_slugify

from django.utils.translation import ungettext_lazy, npgettext_lazy
from django.http import HttpResponse

import findspire.boxes
import findspire.settings
import findspire.models
import findspire.utils.storage


UUID_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
SLUG_BAD_CHARS_RE = re.compile(r'[^a-z0-9_.]+')

def decoded_json(value):
    """Return the value of a base64-encoded JSON object"""
    return json.loads(base64.urlsafe_b64decode(str(value)))

def get_download_url(objects, object_type, object_name):
    ''' Return an URL to download objects '''

    if object_type in objects:
        if 'files' not in objects[object_type]:
            return ""
        if object_name in objects[object_type]['files']:
            obj = objects[object_type]['files'][object_name]
            providers = findspire.utils.storage.get_providers()
            if 'available_on' in obj:
                for provider_name, provider in obj['available_on'].iteritems():
                    if findspire.settings.SNCF:
                        if object_name not in findspire.boxes.BOXES['sizes']:
                            return ''
                        conf = findspire.boxes.BOXES['sizes'][object_name];
                        if conf['height']:
                            return '%s%sfrontend/img/offline/image-%sx%s.jpg' % (findspire.settings.OFFLINE_IMAGES_HOST, findspire.settings.STATIC_URL, conf['width'], conf['height'])
                        return '%s%sfrontend/img/offline/image-%sx.jpg' % (findspire.settings.OFFLINE_IMAGES_HOST, findspire.settings.STATIC_URL, conf['width'])
                    if provider_name in providers:
                        for platform_name, platform in provider.iteritems():
                            if platform_name in providers[provider_name]:
                                download_platform = \
                                    providers[provider_name][platform_name]["download"]

                                upload_platform = \
                                    providers[provider_name][platform_name]["upload"]

                                if download_platform["status"] != "OK":
                                    continue

                                if 'bucket' in platform:
                                    platform = copy.copy(platform)
                                    platform['bucket'] = platform['bucket'].replace('.', '-')

                                if upload_platform["method"] == "golem":
                                    # If the media was uploded on golem, build a valid golem url
                                    platform = copy.copy(platform)
                                    params = upload_platform["params"]
                                    expiration = int(time.time() + 300)  # 300 seconds
                                    uri = "/%s/%s/%s" % (params["client"], platform["bucket"], platform["object"])

                                    platform["expiration"] = expiration
                                    platform["uri"] = uri
                                    platform["key"] = params["public_key"]
                                    platform["verb"] = "GET"

                                    # Compute token
                                    token_string = "%(verb)s%(expiration)d%(uri)sprivate" % platform
                                    token = hmac.new(key=params["private_key"], digestmod=sha512, msg=token_string).hexdigest()
                                    platform["token"] = token

                                return download_platform["url_format"] % platform
    return ""

def find_parent_user_uuid(model):
    """Find the parent user of any model"""
    if "user_uuid" in model:
        return model["user_uuid"]
    elif "parent_user_uuid" in model:
        return model["parent_user_uuid"]

    # First try using the parent profile, then the parent media
    user_uuid = None
    if "parent_profile_uuid" in model:
        profile = findspire.models.Profile.get(model["parent_profile_uuid"])
        if profile is not None:
            user_uuid = find_parent_user_uuid(profile)
    if user_uuid is None and "parent_media_uuid" in model:
        media = findspire.models.Media.get(model["parent_media_uuid"])
        if media is not None:
            user_uuid = find_parent_user_uuid(media)
    return user_uuid

def find_parent_profile_uuids(model):
    """Find all the parent profiles of any model"""
    if model is None:
        return set()
    res = set()
    if "parent_media_uuid" in model and model["parent_media_uuid"] is not None:
        media = findspire.models.Media.get(model["parent_media_uuid"])
        if media is not None:
            res.update(find_parent_profile_uuids(media))
    if "parent_profile_uuid" in model and model["parent_profile_uuid"] is not None:
        parent_profile_uuid = model["parent_profile_uuid"]
        profile = findspire.models.Profile.get(parent_profile_uuid)
        if profile is not None:
            res.add(parent_profile_uuid)
            res.update(find_parent_profile_uuids(profile))
    return res

def get_params(fields, parameters):
    '''
    Construct parameters dict out of URL items
    '''
    # Split parameters by '/' if not None or ""
    parameters = parameters and parameters.split("/") or []
    # parameters must be of fixed lenght, adding more None item, and truncating
    parameters = (parameters + ([None] * len(fields)))[0:len(fields)]

    res = dict(zip(fields, parameters))
    return res

def get_uuid(length=32):
    """Get an UUID."""
    # Fully random string, similar to uuid.uuid4().
    rand = os.urandom(length)
    uuid = long(('%02x'*length) % tuple(map(ord, rand)), 16)
    res = ""
    while uuid > 0:
        uuid, digit = divmod(uuid, len(UUID_ALPHABET))
        res += UUID_ALPHABET[digit]
    # res will very likely be longer than `length` characters. But its length is
    # variable due to null bytes.
    return res[:length]

def get_age(datestr, short_unit=False):
    """Get human readable age from publication"""
    datet = datestr
    if not isinstance(datestr, datetime):
        datet = datetime.strptime(datet, "%Y-%m-%dT%H:%M:%S.%f")
    delta = datetime.utcnow() - datet
    total_seconds = delta.total_seconds()
    age = {}
    if total_seconds < 60:
        age['value'] = int(total_seconds)
        if short_unit:
            age['unit'] = npgettext_lazy('publication age / short unit', 'sec', 'sec', age['value'])
        else:
            age['unit'] = ungettext_lazy('second', 'seconds', age['value'])

    elif total_seconds < 3600:
        age['value'] = int(total_seconds / 60)
        if short_unit:
            age['unit'] = npgettext_lazy('publication age / short unit', 'min', 'min', age['value'])
        else:
            age['unit'] = ungettext_lazy('minute', 'minutes', age['value'])

    elif total_seconds <= 3600*24:
        age['value'] = int(total_seconds / 3600)
        if short_unit:
            age['unit'] = npgettext_lazy('publication age / short unit', 'hour', 'hours', age['value'])
        else:
            age['unit'] = ungettext_lazy('hour', 'hours', age['value'])

    elif delta.days < 31:
        age['value'] = int(delta.days)
        if short_unit:
            age['unit'] = npgettext_lazy('publication age / short unit', 'day', 'days', age['value'])
        else:
            age['unit'] = ungettext_lazy('day', 'days', age['value'])

    elif delta.days < 365:
        age['value'] = int(delta.days / 31)
        if short_unit:
            age['unit'] = npgettext_lazy('publication age / short unit', 'month', 'months', age['value'])
        else:
            age['unit'] = ungettext_lazy('month', 'months', age['value'])

    else:
        age['value'] = int(delta.days / 365)
        if short_unit:
            age['unit'] = npgettext_lazy('publication age / short unit', 'year', 'years', age['value'])
        else:
            age['unit'] = ungettext_lazy('year', 'years', age['value'])

    return age


def normalize_email(email):
    """Normalize an e-mail address

    The normalization converts the domain part to lower-case and converts IDN to Unicode

    >>> normalize_email('thomas@FINDSPIRE.CoM')
    u'thomas@findspire.com'
    >>> normalize_email('test@xn--caf-dma.fr')
    u'test@café.fr'
    >>> normalize_email('test@CAFÉ.FR')
    u'test@café.fr'
    >>> normalize_email(u'test@cafe\u0301.fr')
    u'test@café.fr'
    >>> normalize_email(u'il-fait@xn--quarante-degrs-nkb.xn--gba5j298g.xn--fiqs8s')
    u'il-fait@quarante-degrés.æ©€.中国'
    """
    if type(email) is str:
        email = email.decode("utf-8")
    if '@' not in email:
        return email
    user, domain = email.split("@", 1)
    # Decode Punycode
    try:
        domain = domain.decode("idna")
    except UnicodeError:
        pass
    # Apply nameprep (lower-case, etc.)
    domain = encodings.idna.nameprep(domain)
    return u"%s@%s" % (user.strip(), domain.strip())


def slugify(text, max_length=0):
    """Make a slug from the given text"""
    return py_slugify.slugify(text, separator=".", max_length=max_length)


def clean_slug(text, max_length=0):
    """Clean a user-submitted slug to make sure it matches our standards"""
    # Inspired by the slugify module, without the HTML entity madness.
    # Unicode magic
    if type(text) != types.UnicodeType:
        text = unicode(text, 'utf-8', 'ignore')
    text = unidecode.unidecode(text)
    if type(text) != types.UnicodeType:
        text = unicode(text, 'utf-8', 'ignore')
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore')

    # Remove unwanted characters
    text = text.replace("'", "")

    # Replace invalid characters with a "."
    text = SLUG_BAD_CHARS_RE.sub(".", text.lower())

    # Remove redundant "."
    text = re.sub(r"\.{2,}", ".", text)

    # Truncate to max_length
    if max_length > 0:
        text = text[:max_length]

    return text.strip(".")


def file_md5sum(filename):
    hash_md5 = md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * hash_md5.block_size), b''):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()


class CalledProcessError(Exception):
    def __init__(self, returncode, cmd, output=None, stderr=None):
        super(CalledProcessError, self).__init__(returncode, cmd)
        self.returncode, self.cmd = returncode, cmd
        self.output, self.stderr = output, stderr
    def __str__(self):
        msg = "Command '%s' returned non-zero exit status %d" % (self.cmd, self.returncode)
        if self.stderr:
            msg += "\nStderr:\n" + self.stderr.strip()
        return msg

def check_output_log_stderr(*popenargs, **kwargs):
    """Like subprocess.check_output(), but also logs stderr in the exception."""
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    if 'stderr' in kwargs:
        raise ValueError('stderr argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.PIPE, *popenargs, **kwargs)
    output, stderr = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd, output=output, stderr=stderr)
    return output


# From Python 3.2
class TemporaryDirectory(object):
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everthing contained
    in it are removed.
    """

    def __init__(self, suffix="", prefix="tmp", dir=None):
        # cleanup() needs this and is called even when mkdtemp fails
        self._closed = True
        self.name = tempfile.mkdtemp(suffix, prefix, dir)
        self._closed = False

    def __enter__(self):
        return self.name

    def cleanup(self):
        if not self._closed:
            self._rmtree(self.name)
            self._closed = True

    def __exit__(self, exc, value, tb):
        self.cleanup()

    __del__ = cleanup

    # XXX (ncoghlan): The following code attempts to make
    # this class tolerant of the module nulling out process
    # that happens during CPython interpreter shutdown
    # Alas, it doesn't actually manage it. See issue #10188
    _listdir = staticmethod(os.listdir)
    _path_join = staticmethod(os.path.join)
    _isdir = staticmethod(os.path.isdir)
    _remove = staticmethod(os.remove)
    _rmdir = staticmethod(os.rmdir)
    _os_error = os.error

    def _rmtree(self, path):
        # Essentially a stripped down version of shutil.rmtree.  We can't
        # use globals because they may be None'ed out at shutdown.
        for name in self._listdir(path):
            fullname = self._path_join(path, name)
            try:
                isdir = self._isdir(fullname)
            except self._os_error:
                isdir = False
            if isdir:
                self._rmtree(fullname)
            else:
                try:
                    self._remove(fullname)
                except self._os_error:
                    pass
        try:
            self._rmdir(path)
        except self._os_error:
            pass


def clean_nested_empty_dicts(obj):
    """Recusively remove nested empty dicts.

    This directly modifies `obj`, and returns the updated object.

    >>> clean_nested_empty_dicts({})
    {}
    >>> clean_nested_empty_dicts({'a': {}})
    {}
    >>> clean_nested_empty_dicts({'a': []})
    {'a': []}
    >>> clean_nested_empty_dicts({'a': None})
    {'a': None}
    >>> clean_nested_empty_dicts({'a': {'b': {'c': {'d': {}}, 'e': 1}}, 'f': {}})
    {'a': {'b': {'e': 1}}}
    """
    # If you edit this function, please ensure the doctests still pass!

    if type(obj) is not dict:
        return obj

    for key in obj.keys():
        value = obj[key]
        if type(value) is not dict:
            continue

        clean_nested_empty_dicts(value)
        if len(value) == 0:
            del obj[key]

    return obj


def is_object_available(target, object_type, object_name):
    """ check if an object is available.
    """
    path = ('objects', object_type, 'files', object_name, 'available_on')
    return bool(target.get(path, False))


def default_rejection(request):
    return HttpResponse(status=403)




def request_test_decorator(func, test, rejection=default_rejection):
    '''Decorate a given func with a test, which is a
       function mapping a request object to a boolean.
       If the test fails, then 'rejection' is called.
       Else, the decorated function is called normally. '''
    # This can be applied to functions or class methods. For functions,
    # "request" will be the first argument. For class methods, it will be the
    # second, and the first one SHOULD be "self". This checks if the first
    # argument name is "self" in order to find out what func is.
    # Based on http://stackoverflow.com/a/3564110/113325.
    orig_func = func
    while True:
        try:
            orig_func = orig_func.__wrapped__
        except AttributeError:
            break
    ismethod = inspect.getargspec(orig_func).args[0] == 'self'

    # Use functools.wrap to preserve docstrings, annotations, etc.
    @functools.wraps(func)
    def wrapped_view(*args, **kwargs):
        request = args[1] if ismethod else args[0]
        if test(request):
            return func(*args, **kwargs)
        else:
            return rejection(request)
    wrapped_view.__wrapped__ = func

    return wrapped_view

def get_current_url(request=None, include_lang=False):
    """Return the current URL. Without path and trailing '/'
    eg : https://preprod.findspire.com
    or   http://localhost:8000"""

    if not request:
        request = get_current_request()
    if not request:
        return 'https://www.findspire.com' + ('/en' if include_lang else '')

    host = request.get_host()
    prefix = 'https' if request.is_secure() else 'http'
    if not include_lang:
        return "%s://%s" %(prefix, host)
    return "%s://%s/%s" %(prefix, host, request.language if hasattr(request, "language") else "en")

_not_found = object()
def traverse(d, keys, default=None):
    """ traverse dictionary d with keys

    keys can be an iterable or a dot separated string ex: metadata.basicinfos.name
    """
    if isinstance(keys, basestring):
        keys = keys.split(".")

    current = d
    for k in keys:
        if not hasattr(current, "get"):
            return default
        current = current.get(k, _not_found)
        if current is _not_found:
            return default
    return current


class Filter(object):

    def applicable(self, record):
        return False

    def __call__(self, record):
        return True


class Filtered(object):

    filters = []

    def __init__(self, *filters):
        self._filters = self.filters + list(filters)

    def add(self, f):
        """ add a filter to the stack
        """
        self._filters.append(f)

    def allow(self, record):
        for f in self._filters:
            if hasattr(f, "applicable") and not f.applicable(record):
                continue
            if not f(record):
                return False
        return True

    def filter(self, collection):
        return filter(self.allow, collection)

    def fetch(self, fetcher, size, token, **extra):
        """ returns an iterator that fetch and filter until count is reached.
        :param token: the token to start with
        :param fetcher: is a callable with arguments (size, token).
            - size is how many item you want
            - token will be the last token returned in the previous call.
            it must return results, token.
        :param size: is the batch size.
        :param extra: is passed to fetcher.
        """

        passed = 0
        more = True
        fetched = 0
        last_token = token
        while more and passed < size:
            # stop if we fetched too many element. Probably and infinite loop.
            if fetched > 10 * size:
                raise StopIteration
            items, token = fetcher(size, token, **extra)
            # stop if token
            if not token or last_token == token or len(items) != size:
                more = False
            last_token = token

            for item in items:
                fetched += 1
                if passed >= size:
                    break
                if self.allow(item):
                    passed += 1
                    yield item


def set_publication_status(model, status):
    """ Set the publication status of the given model.

    It also updates child models (think of tracks for an album) and return them.

    :param model: The model to update.
    :param status: The publication status ('published', 'pending', 'private', 'none').
    :return: A list of associated models that have been updated too.
    """
    available_statuses = ('published', 'pending', 'private', 'none')
    if status not in available_statuses:
        raise ValueError('`status` parameter must be one of %s' % (available_statuses,))

    model['publication']['publication_status'] = status

    other_models = []
    # Update album tracks.
    if model['type'] == 'album' and 'child_media_uuids' in model:
        tracks = findspire.models.Media.multiget(model['child_media_uuids']).values()
        for t in tracks:
            if t is None:
                continue
            t['publication']['publication_status'] = status
            other_models.append(t)

    return other_models


if __name__ == "__main__":
    import doctest
    doctest.testmod()
