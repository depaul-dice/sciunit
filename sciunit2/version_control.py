from __future__ import absolute_import

from sciunit2.exceptions import CommandError
from sciunit2.util import quoted_format
import sciunit2.libexec

import subprocess
from subprocess import PIPE
import sys
import os
import shutil
import errno


class Vvpkg(object):
    __slots__ = 'location'

    def __init__(self, location):
        self.location = location

    def checkin(self, rev, pkgdir, spinner):
        cmd = quoted_format('tar cf - -C {1} {2} | {0} commit {3} -',
                            sciunit2.libexec.vv.which,
                            os.getcwd(), pkgdir, rev)
        p = subprocess.Popen(cmd, shell=True, cwd=self.location, stderr=PIPE)
        while p.poll() is None:
            spinner.step()
            spinner.sleep()
        err = p.stderr.read()
        if p.returncode == 0:
            self.cleanup(pkgdir)
            return int(err)
        else:
            raise CommandError('execution %r already exists' % rev
                               if self.__found(rev) else err)

    def checkout(self, rev):
        cmd = quoted_format('{0} checkout {1} - | tar xf -',
                            sciunit2.libexec.vv.which, rev)
        p = subprocess.Popen(cmd, shell=True, cwd=self.location, stderr=PIPE)
        _, err = p.communicate()
        if p.wait() != 0:
            raise CommandError('execution %r not found' % rev
                               if not self.__found(rev) else err)

    def unlink(self, rev):
        try:
            os.unlink(self.__physical(rev))
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise  # pragma: no cover

    def cleanup(self, pkgdir):
        shutil.rmtree(pkgdir, ignore_errors=True)

    def __found(self, rev):
        return os.path.isfile(self.__physical(rev))

    def __physical(self, rev):
        return os.path.join(self.location, '%s.json' % rev)
