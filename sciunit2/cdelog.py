from __future__ import absolute_import
import __builtin__

from sciunit2.util import quoted_format, quoted

import shlex
import json


def open(fn, mode='r'):
    return Script(__builtin__.open(fn, mode))


class Script(object):
    __slots__ = ['__f', '__sh']

    def __init__(self, fp):
        self.__f = fp
        self.__sh = shlex.shlex(self.__f, posix=True)
        self.__sh.whitespace_split = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.__f.close()

    def prepend_cmd(self, args):
        content = self.__f.read()
        self.__f.seek(0)
        self.write_cmd(args)
        self.__f.write(content)

    def write_cmd(self, args):
        self.__f.write('# ')
        json.dump(args, self.__f)
        self.__f.write('\n')

    def read_cmd(self):
        ln = self.__f.readline()
        if ln.startswith('# ['):
            return json.loads(ln[2:])
        else:
            self.__sh.push_source(ln)
            return []

    def __iter__(self):
        return self

    def next(self):
        lno = 0
        ls = []
        while True:
            tok = self.__sh.get_token()
            if tok == self.__sh.eof:
                if ls:
                    break
                else:
                    raise StopIteration
            else:
                ls.append(tok)
                if not lno:
                    lno = self.__sh.lineno
                elif lno < self.__sh.lineno:
                    break
        return ls

    def printf(self, fmt, *args):
        self.__f.write(quoted_format(fmt, *args))

    def insert(self, args):
        print >> self.__f, quoted(args)
