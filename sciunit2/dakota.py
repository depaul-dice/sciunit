from __future__ import absolute_import

from sciunit2.exceptions import CommandError
from sciunit2.util import quoted, make_executable

import tempfile
import subprocess
import os
import re
from distutils.spawn import find_executable


def run(input_file, args=[]):
    exe = find_executable('dakota')
    if exe is None:
        raise CommandError('Dakota environment not setup')
    return subprocess.call(['dakota', '-i', input_file] + args, executable=exe)


class RewroteInputFile(object):
    __slots__ = ['__name', '__orig', '__ptn', '__txt', '__eid', '__driver']

    def __init__(self, orig):
        self.__orig = orig
        self.__ptn = re.compile(r'analysis_drivers\s*=\s*(.*)')
        self.__txt = open(self.__orig).read()
        m = self.__ptn.search(self.__txt)
        if m is None:
            raise CommandError('not a Dakota input file')
        self.__eid = m.group(1)

    def __enter__(self):
        self.__driver = tempfile.NamedTemporaryFile(suffix='.py', delete=False)
        txt = self.__ptn.sub(
            "analysis_drivers = '{0}'".format(self.__driver.name), self.__txt)
        fd, self.__name = tempfile.mkstemp(
            prefix=os.path.basename(self.__orig))
        with os.fdopen(fd, 'w') as fp:
            fp.write(txt)
        return self

    def __exit__(self, *args):
        os.unlink(self.__driver.name)
        os.unlink(self.__name)

    def prepare(self, pkgdir, orig):
        with self.__driver:
            self.__driver.write("""#!/usr/bin/env python2
from sciunit2.cdelog import DetachedExecution
import sciunit2.core
import sciunit2.workspace
import os
import sys

de = DetachedExecution({0!r})
dst = de.cwd_on_host()
os.rename(sys.argv[1], os.path.join(dst, sys.argv[1]))
with open(sys.argv[1], 'a'):
    pass
r = sciunit2.core.repeat({0!r}, {1!r}, sys.argv[1:])
if r == 0:
    os.rename(os.path.join(dst, sys.argv[2]), sys.argv[2])
sys.exit(r)
""".format(pkgdir, orig))
        make_executable(self.__driver.name)

    @property
    def name(self):
        return self.__name

    @property
    def eid(self):
        return self.__eid
