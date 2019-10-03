from __future__ import absolute_import

from sciunit2.exceptions import CommandError, MalformedExecutionId
from sciunit2 import timestamp

import os
import fcntl
import json
import re
from contextlib import closing
from tempfile import NamedTemporaryFile
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
    __slots__ = ['__f', '__pending', '__fn']

    def __init__(self, location):
        self.__fn = os.path.join(location, 'sciunit.db')
        self.__f = bsddb.rnopen(self.__fn)

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
        return Metadata.fromstring(self.__get(self.__to_id(rev)))

    def __get(self, i):
        try:
            return self.__f.db.get(i)
        except KeyError:
            raise CommandError('execution %r not found' % self.__to_rev(i))

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

    def sort(self, revls):
        ls = map(self.__to_id, revls)
        d = set(ls)
        if len(d) < len(ls):
            raise CommandError('duplicated entries')
        mismatched = min(ls)
        rename_list = []

        def need_to_rename(from_, to):
            if to != from_:
                rename_list.append((self.__to_rev(from_), self.__to_rev(to)))

        with NamedTemporaryFile(dir=os.path.dirname(self.__fn)) as fp:
            guard = closing(bsddb.rnopen(fp.name, 'w'))
            with guard as tmp:
                self.__for_upto(mismatched, lambda (k, v): tmp.db.put(k, v))
                for i in ls:
                    j = tmp.db.append(self.__get(i))
                    need_to_rename(i, j)
                self.__for_from(mismatched, lambda (k, v):
                                k not in d and
                                need_to_rename(k, tmp.db.append(v)))

                yield rename_list
                os.rename(fp.name, self.__fn)
                fp.delete = False
                x = self.__f
                self.__f = guard.thing
                guard.thing = x

    def __for_upto(self, last, f):
        with closing(self.__f.db.cursor()) as c:
            try:
                pair = c.first()
                while pair[0] < last:
                    f(pair)
                    pair = c.next()
            except DBNotFoundError:
                pass

    def __for_from(self, first, f):
        with closing(self.__f.db.cursor()) as c:
            pair = c.set(first)
            while True:
                f(pair)
                try:
                    pair = c.next()
                except DBNotFoundError:
                    break

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
