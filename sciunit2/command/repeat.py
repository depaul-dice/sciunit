from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
import sciunit2.core
import sciunit2.workspace

from getopt import getopt
import sys
import os


class RepeatCommand(AbstractCommand):
    name = 'repeat'

    @property
    def usage(self):
        return [('repeat <execution id> [<args...>]',
                 "Repeat the execution of <execution id>")]

    def run(self, args):
        optlist, args = getopt(args, '')
        if not args:
            raise CommandLineError
        emgr, repo = sciunit2.workspace.current()
        with emgr.exclusive():
            orig = emgr.get(args[0]).cmd
            pkgdir = os.path.join(repo.location, 'cde-package')
            repo.cleanup(pkgdir)
            repo.checkout(args[0])
            sys.exit(sciunit2.core.repeat(pkgdir, orig, args[1:]))
