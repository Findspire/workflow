#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright 2013 Findspire

"""File part of Findspire frontend project, used to handle upload functions"""

import hashlib
import hmac
import logging
import os.path
import re
import threading
import time

import findspire.utils.storage
from findspire.utils import utils

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import requests

logger = logging.getLogger(__name__)
sessions = threading.local()

class UploadError(Exception):
    pass

# Map object types to S3 bucket types
UPLOAD_TYPES = {
    r"image$": "image",
    r"(?:album|playlist)_cover$": "image",
    r"profile_picture$": "image",
    r"profile_page_background$": "image",
    r"poster$": "image",
    r"track$": "audio",
    r"video(?:-sample)?$": "video",
    r"video_cover-(?:custom|source)-[0-9]+$": "image",
}

def get_upload_type(upload_type):
    """Get the type (image, audio, video) for an object name (image, album_cover, track...)

    >>> get_upload_type('image')
    'image'
    >>> get_upload_type('profile_picture')
    'image'
    >>> get_upload_type('album_cover')
    'image'
    >>> get_upload_type('video_cover-custom-08')
    'image'
    >>> get_upload_type('track')
    'audio'
    >>> get_upload_type('video')
    'video'
    >>> get_upload_type('video-sample')
    'video'
    """
    for entry, entry_type in UPLOAD_TYPES.iteritems():
        if re.match(entry, upload_type):
            return entry_type
    return None

def upload_to_put_storage(upload_settings, bucket_name, object_name, mime_type, filep=None, filepath=None, public=True):
    """Upload to storage using PUT"""
    params = {"bucket": bucket_name, "object": object_name}
    url = upload_settings["url_format"] % params
    if url.startswith("//"):
        url = "http:" + url
    if not filep:
        filep = open(filepath)

    filep.seek(0, 2)
    file_size = filep.tell()
    filep.seek(0)

    sess = None
    if hasattr(sessions, "put_sess"):
        sess = sessions.put_sess
    if sess is None:
        sess = requests.Session()
        sessions.put_sess = sess

    time_start = time.time()
    res = sess.put(url, data=filep)
    time_taken = time.time() - time_start

    res.text  # read the body to reuse connection
    logger.info("Put upload took %.3f seconds for %.3f MB (%.3f MB/s); status: %d",
                time_taken, file_size/1e6, file_size/(time_taken * 1e6), res.status_code)

    if not 200 <= res.status_code < 300:
        raise UploadError("put: upload failed for %s/%s: code %d" % (bucket_name, object_name, res.status_code))
    return params

def upload_to_s3(upload_settings, bucket_name, object_name, mime_type, filep=None, filepath=None, public=True):
    """Upload to storage using S3"""
    conn = S3Connection(**upload_settings["params"])

    bucket = conn.lookup(bucket_name)
    if bucket is None:
        bucket = conn.create_bucket(bucket_name, location=upload_settings['location'])
        if public:
            bucket.set_acl('public-read')
    k = Key(bucket)
    k.key = object_name
    if filepath:
        k.set_contents_from_filename(filepath, headers={'Content-Type': mime_type})
    else:
        k.set_contents_from_file(filep, headers={'Content-Type': mime_type})

    if public:
        k.set_acl('public-read')
    return {"bucket": bucket_name, "object": object_name}


def golem_params(upload_settings, verb, uri, flag, expiry=24*3600):
    params = upload_settings["params"]
    expiration = int(time.time() + expiry)  # 24 hours
    token_string = "%(verb)s%(expiration)d%(uri)s%(flag)s" % {
        "verb": verb,
        "expiration": expiration,
        "uri": uri,
        "flag": flag,
    }
    token = hmac.new(key=params["private_key"], digestmod=hashlib.sha512,
                     msg=token_string).hexdigest()
    return {
        "expiration": expiration,
        "token": token,
        "key": params["public_key"],
        "flag": flag,
    }


def golem_url_and_params(upload_settings, verb, bucket_name, object_name, public=True, expiry=24*3600):
    params = upload_settings["params"]
    flag = "public" if public else "private"
    uri = "/%s/%s/%s" % (params["client"], bucket_name, object_name)
    url = "http://%(hostname)s%(uri)s" % {
        "hostname": params["hostname"],
        "uri": uri,
    }
    url_params = golem_params(upload_settings, verb, uri, flag, expiry=expiry)
    return url, url_params


def golem_client():
    sess = None
    if hasattr(sessions, "golem_sess"):
        sess = sessions.golem_sess
    if sess is None:
        sess = requests.Session()
        sessions.golem_sess = sess
    return sess


def delete_from_golem(upload_settings, bucket_name, object_name):
    """ delete a file from golem server
    """
    url, url_params = golem_url_and_params(
        upload_settings, "DELETE", bucket_name, object_name, public=False)

    session = golem_client()
    r = session.delete(url, params=url_params)
    r.text  # read the body to reuse connection
    return r.status_code == 204 or r.status_code == 404


def upload_to_golem(upload_settings, bucket_name, object_name, mime_type, filep=None, filepath=None, public=True):
    """Upload to a Golem server"""
    url, url_params = golem_url_and_params(
        upload_settings, "PUT", bucket_name, object_name, public=public)

    if filep is None:
        filep = open(filepath, "rb")
    filep.seek(0)

    md5 = hashlib.md5()
    for chunk in iter(lambda: filep.read(128 * md5.block_size), b""):
        md5.update(chunk)
    md5 = md5.hexdigest()

    filep.seek(0, 2)
    file_size = filep.tell()
    filep.seek(0)

    sess = golem_client()
    time_start = time.time()
    res = sess.put(url, params=url_params, data=filep)
    time_taken = time.time() - time_start
    logger.info("Golem upload took %.3f seconds for %.3f MB (%.3f MB/s); status: %d",
                time_taken, file_size/1e6, file_size/(time_taken * 1e6), res.status_code)

    res.text  # read the body to reuse connection
    if 200 <= res.status_code < 300:
        if "etag" not in res.headers:
            raise UploadError("golem: ETag is missing after uploading %s/%s" % (bucket_name, object_name))

        etag = res.headers["etag"].strip('"')
        if etag != md5:
            raise UploadError("golem: invalid checksum for %s/%s: expected %s, got %s"
                              % (bucket_name, object_name, etag, md5))
            # TODO: try to remove from the server

        # Success
        return {"bucket": bucket_name, "object": object_name}

    else:
        raise UploadError("golem: upload failed for %s/%s: code %d: %s" % (bucket_name, object_name, res.status_code, res.text))

UPLOAD_METHODS = {
    "put": upload_to_put_storage,
    "s3": upload_to_s3,
    "golem": upload_to_golem,
}

def get_uploaders(upload_type):
    """Get valid platforms for the given upload type.

    :param upload_type: image, audio, upload, hls-audio, etc.
    :return: [(provider_name, platform_name, upload_function)]
    """
    res = []
    providers = findspire.utils.storage.get_providers()
    for provider_name, provider in providers.iteritems():
        for platform_name, platform in provider.iteritems():
            if platform["upload"]["status"] == "OK" and \
               ((upload_type == "upload" and "upload_bucket" in platform["upload"]) \
                or upload_type in platform["upload"]["media_bucket"]):
                entry = (provider_name, platform_name, UPLOAD_METHODS[platform["upload"]["method"]])
                res.append(entry)
    return res

def upload_file(media_uuid, object_type, object_name, file_name, mime_type,
                filepath=None, filep=None, public=True, obj_metadata=None,
                upload_type=None):
    """Upload file to all available storage providers.

    :param media_uuid: UUID of the media
    :param object_type: type of the uploaded object: image, video, video_cover, album_cover, etc.
    :param object_name: name of the uploaded object: square, preview, source, etc.
    :param file_name: name of the uploaded key: video_cover-source-01-source, etc.
    :param mime_type: MIME type of the uploaded file:
    :param filepath: path to the uploaded file
    :param filep: an open file descriptor for the uploaded file
    :param public: a boolean indicating whether the uploaded file should be accessible by everyone on the wild Internet
    :param obj_metadata: a dict of additional __metadata__ for the uploaded file
    :param upload_type: override the upload_type automatic selection.
    :return: an `objects` dictionary
    """
    files = {}
    if filepath:
        file_size = os.path.getsize(filepath)
    else:
        file_size = os.fstat(filep.fileno()).st_size
    providers = findspire.utils.storage.get_providers()
    upload_type = upload_type or get_upload_type(object_type)

    for provider_name, platform_name, uploader in get_uploaders(upload_type):
        bucket, key = findspire.utils.storage.format_bucket_and_key(provider_name, platform_name, upload_type,
                                                                    media_uuid, utils.get_uuid(16) + "-" + file_name)
        if bucket is None or key is None:
            continue
        if hasattr(filep, "seek"):
            filep.seek(0)
        platform = providers[provider_name][platform_name]
        platform_result = uploader(platform["upload"], bucket, key, mime_type, filep=filep, filepath=filepath,
                                   public=public)
        if platform_result:
            files.setdefault(provider_name, {})
            files[provider_name].setdefault(platform_name, {})
            files[provider_name][platform_name] = platform_result

    if obj_metadata is None:
        obj_metadata = {}
    obj_metadata["size"] = file_size
    return {"objects": {object_type: {"files": {object_name: {
        "available_on": files,
        "__metadata__": obj_metadata
    }}}}}
