from __future__ import absolute_import

from sciunit2.exceptions import CommandError, MalformedExecutionId

import os
import fcntl
import json
from utcdatetime import utcdatetime
from contextlib import closing
try:
    import bsddb3 as bsddb
except ImportError:
    import bsddb


class Metadata(object):
    __slots__ = '__d'

    def __init__(self, args):
        if isinstance(args, list):
            self.__d = {'cmd': args, 'started': str(utcdatetime.now())}
        else:
            self.__d = json.loads(args)

    def __str__(self):
        return json.dumps(self.__d, separators=(',', ':'))

    @classmethod
    def fromstring(cls, s):
        return cls(s)

    @property
    def cmd(self):
        return self.__d['cmd']

    @property
    def started(self):
        return self.__d['started']


class ExecutionManager(object):
    __slots__ = ['__f', '__pending']

    def __init__(self, location):
        self.__f = bsddb.rnopen(os.path.join(location, 'sciunit.db'), 'c')

    def close(self):
        self.__f.close()

    def exclusive(self):
        fcntl.flock(self.__f.db.fd(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return closing(self)

    def shared(self):
        fcntl.flock(self.__f.db.fd(), fcntl.LOCK_SH | fcntl.LOCK_NB)
        return closing(self)

    def add(self, args):
        try:
            newid = self.__f.last()[0] + 1
        except bsddb._db.DBNotFoundError:
            newid = 1
        self.__pending = (newid, Metadata(args))
        return 'e%d' % newid

    def commit(self):
        k, v = self.__pending
        self.__f[k] = str(v)

    def get(self, rev):
        try:
            if not rev.startswith('e'):
                raise ValueError
            k = int(rev[1:])
        except ValueError:
            raise MalformedExecutionId
        try:
            return Metadata.fromstring(self.__f[k])
        except KeyError:
            raise CommandError('execution %r not found' % rev)
