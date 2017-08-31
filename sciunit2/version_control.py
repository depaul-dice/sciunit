from __future__ import absolute_import

from sciunit2.exceptions import CommandError
from sciunit2.util import quoted_format, Chdir
import sciunit2.libexec

import subprocess
from subprocess import PIPE
import sys
import os
import shutil
from glob import glob
import re


class Vvpkg(object):
    __slots__ = 'location'

    def __init__(self, location):
        self.location = location

    def next_rev(self):
        with Chdir(self.location):
            ls = glob('e*.json')
        mls = [re.match(r'e(\d+)\.json', s) for s in ls]
        dls = [int(s.group(1)) for s in mls if s is not None]
        return 'e%d' % (max(dls) + 1 if dls else 1)

    def checkin(self, pkgdir):
        rev = self.next_rev()
        cmd = quoted_format('tar cf - {1} | {0} commit {2} -',
                            sciunit2.libexec.vv.location,
                            os.path.abspath(pkgdir), rev)
        p = subprocess.Popen(cmd, shell=True, cwd=self.location, stderr=PIPE)
        _, err = p.communicate()
        if p.wait() == 0:
            self.cleanup(pkgdir)
            return rev
        else:
            raise CommandError(err)

    def cleanup(self, pkgdir):
        shutil.rmtree(pkgdir, ignore_errors=True)
