from __future__ import absolute_import

from sciunit2.exceptions import CommandError, MalformedExecutionId
from sciunit2 import timestamp

import os
import fcntl
import json
import re
from contextlib import closing
try:
    import bsddb3 as bsddb
except ImportError:
    import bsddb
DBNotFoundError = bsddb._db.DBNotFoundError


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

    @property
    def size(self):
        return self.__d['size']

    @size.setter
    def size(self, val):
        self.__d['size'] = val


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
        except DBNotFoundError:
            newid = 1
        self.__pending = (newid, Metadata(args))
        return self.__to_rev(newid)

    def commit(self, size):
        k, v = self.__pending
        v.size = size
        self.__f[k] = str(v)
        return (self.__to_rev(k), v)

    def get(self, rev):
        try:
            return Metadata.fromstring(self.__f[self.__to_id(rev)])
        except KeyError:
            raise CommandError('execution %r not found' % rev)

    def last(self):
        id_, m = self.__f.last()
        return (self.__to_rev(id_), Metadata.fromstring(m))

    def delete(self, rev):
        try:
            del self.__f[self.__to_id(rev)]
        except KeyError:
            pass

    def deletemany(self, revrange):
        bg, ed = self.__to_id_range(revrange)
        with closing(self.__f.db.cursor()) as c:
            try:
                if ed is None:
                    p = c.last()
                    ed = p[0]
                else:
                    # XXX set_range not functioning
                    try:
                        p = c.set(ed)
                    except bsddb._db.DBError:
                        p = c.last()

                while not p[0] < bg:
                    if not ed < p[0]:
                        c.delete()
                        yield self.__to_rev(p[0])
                    p = c.prev()

            except DBNotFoundError:
                pass

    @staticmethod
    def __to_rev(id_):
        return 'e%d' % id_

    @staticmethod
    def __to_id(rev):
        if not re.match(r'^e[1-9]\d*$', rev):
            raise MalformedExecutionId
        return int(rev[1:])

    @staticmethod
    def __to_id_range(revrange):
        r = re.match(r'^e([1-9]\d*)-([1-9]\d*)?$', revrange)
        if not r:
            raise MalformedExecutionId
        return tuple(int(x) if x is not None else x for x in r.groups())

    def list(self):
        for k, v in self.__f.iteritems():
            yield self.__to_rev(k), Metadata.fromstring(v)
