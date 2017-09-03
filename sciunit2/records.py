from __future__ import absolute_import

from sciunit2.exceptions import CommandError, MalformedExecutionId
from sciunit2 import timestamp

import os
import fcntl
import json
from contextlib import closing
try:
    import bsddb3 as bsddb
except ImportError:
    import bsddb


class Metadata(object):
    __slots__ = '__d'

    def __init__(self, args):
        if isinstance(args, list):
            self.__d = {'cmd': args, 'started': str(timestamp.now())}
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
        return timestamp.fromstring(self.__d['started'])


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
            return Metadata.fromstring(self.__f[self.__to_id(rev)])
        except KeyError:
            raise CommandError('execution %r not found' % rev)

    def delete(self, rev):
        try:
            del self.__f[self.__to_id(rev)]
        except KeyError:
            pass

    @staticmethod
    def __to_id(rev):
        try:
            if not rev.startswith('e'):
                raise ValueError
            return int(rev[1:])
        except ValueError:
            raise MalformedExecutionId

    def list(self):
        for k, v in self.__f.iteritems():
            yield 'e%d' % k, Metadata.fromstring(v)
