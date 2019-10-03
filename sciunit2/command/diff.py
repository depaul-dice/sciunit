#Note: Converted
from __future__ import absolute_import

from sciunit2.command import AbstractCommand
#from sciunit2.command.mixin import CommitMixin
from sciunit2.exceptions import CommandLineError, CommandError
from sciunit2.command.context import CheckoutContext
#from sciunit2.cdelog import DetachedExecution
import sciunit2.workspace
from sciunit2.util import quoted_format

from getopt import getopt
import os
import subprocess
from subprocess import PIPE


class DiffCommand(AbstractCommand):
    name = 'diff'

    @property
    def usage(self):
        return [('diff <execution id1> <execution id2>',
                 'Compare two execution containers file by file. ')]

    def run(self, args):
        optlist, args = getopt(args, '') # <execution id1> <execution id2>
        if len(args) <= 1:
            raise CommandLineError
        emgr, repo = sciunit2.workspace.current()

        with emgr.exclusive():
            orig1 = emgr.get(args[0]).cmd
            diffdir = os.path.join(repo.location, 'Diff')
            repo.checkout_Diff(args[0])
            orig2 = emgr.get(args[1]).cmd
            repo.checkout_Diff(args[1])
            cmd = quoted_format('diff -qr {0} {1}', args[0], args[1])
            p = subprocess.Popen(cmd, shell=True, cwd=diffdir, stderr=PIPE, stdout=PIPE)
            out, err = p.communicate()
            p_status = p.wait()
            return (out, err)

    def note(self, aList):
        return "\n %s \n %s \n" % (aList[0].decode('utf-8'), aList[1].decode('utf-8'))

        #emgr, repo = sciunit2.workspace.current()
        #pkgdir = os.path.join(repo.location, 'cde-package')
        #with emgr.exclusive():
        #    for cmd in DetachedExecution(pkgdir).getcmd():
        #        rev = emgr.add(cmd)
        #        return self.do_commit(pkgdir, rev, emgr, repo)
        #    else:
        #        raise CommandError('nothing to commit')
