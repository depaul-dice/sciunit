from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
import sciunit2.core

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
        repo = sciunit2.workspace.repo()
        repo.checkout(args[0])
        sys.exit(sciunit2.core.repeat(
            os.path.join(repo.location, 'cde-package'), args[1:]))
