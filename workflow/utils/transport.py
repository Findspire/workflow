# -*- coding: utf-8 -*-
# Copyright 2014 Findspire

"""Local and remote transports"""

from abc import ABCMeta, abstractmethod
from cStringIO import StringIO
from collections import namedtuple
from datetime import datetime
import errno
import ftplib
import os.path
import stat
import tempfile
import time
import urllib2

import paramiko
import paramiko.rsakey
import pytz

Stat = namedtuple("Stat", ["st_mode", "st_uid", "st_gid", "st_size", "st_mtime"])


class FileTransport(object):
    __metaclass__ = ABCMeta
    scheme = "file"

    def __init__(self, config):
        self._config = config

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def put(self, fd, path):
        pass

    @abstractmethod
    def list(self, path):
        pass

    @abstractmethod
    def list_stat(self, path):
        """List and return (filename, Stat object) collection."""
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def open(self, filename):
        pass

    @abstractmethod
    def move(self, src, dest):
        pass

    @abstractmethod
    def mkdir(self, path):
        pass

    def normalize_path(self, path):
        basedir = self._config.get('basedir')
        if not basedir:
            return path
        return os.path.join(basedir, path)

    def create_basedir(self):
        if not 'basedir' in self._config:
            return
        basedir = self._config.pop('basedir')
        path = '/' if os.path.isabs(basedir) else ''
        for directory in basedir.split('/'):
            path = '{}{}/'.format(path, directory)
            try:
                self.mkdir(path)
            except:
                pass
        self._config['basedir'] = basedir


class FTPTransport(FileTransport):
    scheme = "ftp"

    @property
    def conn(self):
        if hasattr(self, '_conn'):
            return self._conn
        return None

    def connect(self):
        print self._config
        if 'port' in self._config:
            self._conn = ftplib.FTP()
            self._conn.connect(self._config['host'], self._config['port'])
        else:
            self._conn = ftplib.FTP(self._config['host'])
        self._conn.login(user=self._config['username'], passwd=self._config['password'])
        self.create_basedir()

    def put(self, fd, path):
        path = self.normalize_path(path)
        fd.flush()
        fd.seek(0)
        self._conn.storlines("STOR %s" % path, fd)

    def list(self, path):
        path = self.normalize_path(path)
        return sorted(self._conn.nlst(path))

    def move(self, src, dst):
        src = self.normalize_path(src)
        dst = self.normalize_path(dst)
        return self._conn.rename(src, dst)

    def close(self):
        return self._conn.close()

    def list_stat(self, path):
        path = self.normalize_path(path)
        lines = []
        stats = []
        self._conn.retrlines("MLSD %s" % path, lines.append)
        for line in lines:
            info, filename = line.strip().split(" ", 2)
            attrs = {key.lower(): value for key, value in [a.split("=", 2) for a in info.split(";") if a]}
            mtime = datetime.strptime(attrs['modify'], "%Y%m%d%H%M%S").replace(tzinfo=pytz.UTC)
            st = Stat(
                st_size=int(attrs.get('size', '0')),
                st_mtime=time.mktime(mtime.timetuple()),
                st_uid=int(attrs.get("UNIX.uid", "0")),
                st_gid=int(attrs.get("UNIX.gid", "0")),
                st_mode=int(attrs.get("UNIX.mode", "0"), 8))
            if st.st_mode in ('dir', 'cdir', 'pdir'):
                st.st_mode &= stat.S_IFDIR
            stats.append((filename, st))
        return stats

    def open(self, path):
        path = self.normalize_path(path)
        url = "ftp://%s:%s@%s" % (self._config['username'], self._config['password'], self._config['host'])
        return urllib2.urlopen(os.path.join(url, path))

    def mkdir(self, path):
        path = self.normalize_path(path)
        self._conn.mkd(path)


class SFTPTransport(FileTransport):
    scheme = "sftp"

    @property
    def conn(self):
        if hasattr(self, '_conn'):
            return self._conn
        return None

    def connect(self):
        transport = getattr(self, '_transport', None)
        if transport is None:
            transport = paramiko.transport.Transport(self._config['host'])

            pkey = None
            if 'pkey' in self._config:
                pkey = paramiko.rsakey.RSAKey(file_obj=StringIO(self._config['pkey']))

            transport.connect(
                username=self._config['username'],
                password=self._config.get('password', None),
                pkey=pkey)
            self._transport = transport

        self._conn = paramiko.SFTPClient.from_transport(transport)
        self.create_basedir()
        return self

    def get(self, path):
        # FIXME implement this in other transports as well
        path = self.normalize_path(path)
        fd = tempfile.NamedTemporaryFile()
        self._conn.getfo(path, fd)
        fd.flush()
        os.fsync(fd.fileno())
        fd.seek(0)
        return fd

    def put(self, fd, path):
        path = self.normalize_path(path)
        fd.flush()
        fd.seek(0, os.SEEK_END)
        size = fd.tell()
        fd.seek(0)
        channel = self._conn.get_channel()
        with channel.lock:
            channel.out_window_size += size
            channel.out_buffer_cv.notifyAll()
        self._conn.putfo(fd, path)
        return

    def list(self, path):
        path = self.normalize_path(path)
        return sorted(self._conn.listdir(path))

    def list_stat(self, path):
        path = self.normalize_path(path)
        return [(s.filename, s) for s in self._conn.listdir_attr(path)]

    def move(self, src, dst):
        src = self.normalize_path(src)
        dst = self.normalize_path(dst)
        return self._conn.rename(src, dst)

    def close(self):
        self._conn.close()
        return self._transport.close()

    def open(self, path):
        path = self.normalize_path(path)
        return self._conn.file(path, 'r')

    def mkdir(self, path):
        path = self.normalize_path(path)
        self._conn.mkdir(path)


class LocalTransport(FileTransport):
    def connect(self):
        self.create_basedir()

    def put(self, fd, path):
        path = self.normalize_path(path)
        fd.flush()
        fd.seek(0)
        with open(path, 'w') as destfile:
            for chunk in fd:
                destfile.write(chunk)

    def list(self, path):
        path = self.normalize_path(path)
        return sorted(os.listdir(path))

    def list_stat(self, path):
        path = self.normalize_path(path)
        items = []
        for p in os.listdir(path):
            items.append(
                (p, os.stat(os.path.join(path, p))))
        return items

    def move(self, src, dst):
        src = self.normalize_path(src)
        dst = self.normalize_path(dst)
        return os.rename(src, dst)

    def close(self):
        pass

    def open(self, path):
        path = self.normalize_path(path)
        return open(path, 'r')

    def mkdir(self, path):
        path = self.normalize_path(path)
        try:
            return os.mkdir(path)
        except OSError, err:
            if err.errno != errno.EEXIST:
                raise err
