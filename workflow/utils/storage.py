#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013 Findspire

"""File part of Findspire frontend project, used to handle storage providers."""

from findspire import settings

import hashlib
import hmac
import json
import random
import os
import os.path
import tempfile
import threading
import time
import weakref

import boto
import boto.s3.connection
import redis
import requests

import findspire.apps.tasks

# Data structure used to cache local FDs for files downloaded from the cache. A
# cache cache!
# Using weak references to ensure that temporary files are garbage-collected
# when they are not used anymore.
CACHE_CACHE_LOCK = threading.Lock()
CACHE_CACHE = weakref.WeakValueDictionary()

def add_to_local_cache(fd, urn, object_type, object_name):
    """Add a file object to the local cache.

    :param fd: File object
    :param urn: URN string of the model (Media or Profile) owning that object
    :param object_type: the object type (image, video, track...)
    :param object_name: the object name (source, mp4-hq, ogg...)
    """
    cache_cache_key = (urn, object_type, object_name)
    with CACHE_CACHE_LOCK:
        CACHE_CACHE[cache_cache_key] = fd

def get_from_local_cache(urn, object_type, object_name):
    """Get a file object from the local cache.

    :param urn: URN string of the model (Media or Profile) owning that object
    :param object_type: the object type (image, video, track...)
    :param object_name: the object name (source, mp4-hq, ogg...)
    :return: a file object, or None of not available
    """
    cache_cache_key = (urn, object_type, object_name)
    with CACHE_CACHE_LOCK:
        cached_fd = CACHE_CACHE.get(cache_cache_key, None)
        if cached_fd is not None and hasattr(cached_fd, "closed") and not cached_fd.closed:
            cached_fd.seek(0)
            return cached_fd
    return None


def get_providers():
    ''' Return all providers '''
    if settings.STORAGE_REDIS is not None:
        host, port = settings.STORAGE_REDIS
        red = redis.StrictRedis(host, port)
        conf = red.get("storage_providers")
        return json.loads(conf)
    else:
        return settings.STORAGE_PROVIDERS

def choose_upload_provider(media_type):
    """Return a valid upload (provider, platform, params) tuple

    :param media_type: the media type: image, audio, video, upload, hls-audio…
    :return: a (provider, platform, upload_params, download_params) tuple"""
    providers = get_providers()
    choices = []
    for provider_name, provider in providers.iteritems():
        for platform_name, platform in provider.iteritems():
            if "upload" in platform and platform["upload"]["status"] == "OK" \
               and ((media_type == "upload" and "upload_bucket" in platform["upload"])
                    or media_type in platform["upload"]["media_bucket"]):
                choices.append((provider_name, platform_name, platform["upload"], platform["download"]))
    return random.choice(choices)

def format_bucket_and_key(provider, platform, media_type, media_uuid, file_name):
    """Return (bucket, key) for the given parameters"""
    providers = get_providers()
    upload = providers[provider][platform]["upload"]
    params = {
        "media_uuid": media_uuid,
        "file_name": file_name,
    }
    if media_type == "upload" and "upload_bucket" in upload:
        bucket_fmt = upload["upload_bucket"]
    elif media_type not in upload["media_bucket"]:
        return None, None
    else:
        bucket_fmt = upload["media_bucket"][media_type]
    return (bucket_fmt % params, upload["object_key"] % params)


def download_object(avail_on, expected_size=None, dir=None):
    """Download an object to a temporary file using the best available method. This
       is suitable for (private) sources stored on S3 as it will use boto to fetch
       them."""

    providers = get_providers()
    params, bucket_name, object_name = None, None, None

    for provider_name, provider_data in avail_on.iteritems():
        for platform_name, platform_data in provider_data.iteritems():
            if provider_name in providers and platform_name in providers[provider_name] \
               and "download" in providers[provider_name][platform_name] \
               and providers[provider_name][platform_name]["download"]["status"] == "OK":
                provider = providers[provider_name][platform_name]
                params = provider['upload']
                bucket_name = platform_data['bucket']
                object_name = platform_data['object']
                break

    tmpf = tempfile.NamedTemporaryFile(dir=dir or settings.TEMPORARY_DOWNLOAD_FOLDER)
    if params["method"] == "s3":
        # S3 version
        boto_conn = boto.s3.connection.S3Connection(**params['params'])
        bucket = boto_conn.get_bucket(bucket_name, validate=False)
        key = bucket.get_key(object_name)
        key.get_file(tmpf)

    elif params["method"] == "put":
        # PUT version
        url = provider['upload']['url_format'] % {'bucket': bucket_name, 'object': object_name}
        if url.startswith("//"):
            url = "http:" + url
        res = requests.get(url, stream=True)
        for chunk in res.iter_content(chunk_size=512*1024):
            tmpf.write(chunk)

    elif params["method"] == "golem":
        # Golem version
        expiration = int(time.time() + 24*3600)  # 24 hours
        uri = "/%s/%s/%s" % (params["params"]["client"], bucket_name, object_name)
        token_string = "%(verb)s%(expiration)d%(uri)sprivate" % {"verb": "GET", "expiration": expiration, "uri": uri}
        token = hmac.new(key=params["params"]["private_key"], digestmod=hashlib.sha512, msg=token_string).hexdigest()
        url = "http://%s%s" % (params["params"]["hostname"], uri)
        url_params = {"expiration": expiration, "token": token, "key": params["params"]["public_key"]}
        res = requests.get(url, params=url_params, stream=True)

        if res.status_code < 200 or res.status_code > 300:
            raise Exception("golem download failed: %s: %s" % (res.status_code, res.text))

        md5 = hashlib.md5()
        for chunk in res.iter_content(chunk_size=512*1024):
            tmpf.write(chunk)
            md5.update(chunk)

        md5 = md5.hexdigest()
        if "etag" in res.headers:
            etag = res.headers["etag"].strip('"')
            if md5 != etag:
                raise Exception("Invalid MD5 for downloaded object %s/%s: expected %s, got %s"
                                % (bucket_name, object_name, etag, md5))

    else:
        raise ValueError("Unknown download method: " + params["method"])

    tmpf.flush()
    os.fsync(tmpf.fileno())
    tmpf.seek(0)

    # Size check
    tmpf_size = os.path.getsize(tmpf.name)
    if expected_size is None or tmpf_size == expected_size:
        return tmpf
    else:
        raise Exception("Invalid size for downloaded object %s/%s: expected %d, got %d"
                        % (bucket_name, object_name, expected_size, tmpf_size))


def upload_to_cache(srcf, urn, object_type, object_name):
    """Upload an local file to the local WebDAV cache.

    :param srcf: the file file-like object to upload
    :param urn: URN of the model (Media or Profile) owning that object
    :param object_type: the object type (image, video, track...)
    :param object_name: the object name (source, mp4-hq, ogg...)
    """
    srcf.seek(0)
    url = settings.FILECACHE_URL % {"uuid": urn, "type": object_type, "name": object_name}
    if url.startswith("//"):
        url = "http:" + url
    requests.put(url, data=srcf)
    findspire.apps.tasks.upload.delete_from_cache.apply_async((urn, object_type, object_name),
                                                              countdown=settings.FILECACHE_EXPIRATION_DELAY)

def download_from_cache(model, object_type, object_name, dir=None):
    """Download an object to a local (temporary) file, preferably from the local
    WebDAV cache.

    :param model: the Media or Profile instance that contains the object to download
    :param object_type: the object type (image, video, track...)
    :param object_name: the object name (source, mp4-hq, ogg...)
    """

    object_size = model.get(('objects', object_type, 'files', object_name, '__metadata__', 'size'), None)
    cached_fd = get_from_local_cache(model.urn_s, object_type, object_name)
    if cached_fd is not None:
        return cached_fd

    if object_type != "track":
        # Try fetching from cache first
        url = settings.FILECACHE_URL % {"uuid": model.urn_s, "type": object_type, "name": object_name}
        if url.startswith("//"):
            url = "http:" + url
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            tmpf = tempfile.NamedTemporaryFile(dir=dir or settings.TEMPORARY_DOWNLOAD_FOLDER)
            for chunk in res.iter_content(chunk_size=512*1024):
                tmpf.write(chunk)
            tmpf.flush()
            os.fsync(tmpf.fileno())
            tmpf.seek(0)

            # Size check
            tmpf_size = os.path.getsize(tmpf.name)
            if object_size is None or object_size == tmpf_size:
                return tmpf
            elif object_size != tmpf_size:
                print "Invalid size for cache file, downloading from storage provider.."

    # If it failed, download from remote, and upload to cache
    avail_on = model[('objects', object_type, 'files', object_name, 'available_on')]
    tmpf = download_object(avail_on, object_size, dir=dir)
    if object_type != "track":
        upload_to_cache(tmpf, model.urn_s, object_type, object_name)
    tmpf.seek(0)

    # Add the downloaded file to the cache cache
    add_to_local_cache(tmpf, model.urn_s, object_type, object_name)

    return tmpf

def delete_from_cache(urn, object_type, object_name):
    """Delete a file to the local WebDAV cache.

    :param urn: URN of the model (Media or Profile) owning that object
    :param object_type: the object type (image, video, track...)
    :param object_name: the object name (source, mp4-hq, ogg...)
    """

    url = settings.FILECACHE_URL % {"uuid": urn, "type": object_type, "name": object_name}
    if url.startswith("//"):
        url = "http:" + url
    requests.delete(url)
