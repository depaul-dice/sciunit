from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
from sciunit2.util import quoted
from sciunit2 import timestamp
import sciunit2.workspace

from getopt import getopt


class RmCommand(AbstractCommand):
    name = 'rm'

    @property
    def usage(self):
        return [('rm <execution id>', 'Remove an execution from the sciunit')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if len(args) != 1:
            raise CommandLineError
        emgr, repo = sciunit2.workspace.current()
        with emgr.exclusive():
            emgr.delete(args[0])
            repo.unlink(args[0])
