from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
import sciunit2.core

from getopt import getopt


class ExecCommand(AbstractCommand):
    name = 'exec'

    @property
    def usage(self):
        return [('exec <executable> [<args...>]',
                 'Capture the execution of the given command line'),
                ('exec -i',
                 "Capture the user's interactions inside a shell")]

    def run(self, args):
        optlist, args = getopt(args, 'i')
        if optlist:
            if args:
                raise CommandLineError
            repo = sciunit2.workspace.repo()
            sciunit2.core.shell()
        else:
            if not args:
                raise CommandLineError
            repo = sciunit2.workspace.repo()
            sciunit2.core.capture(args)
        repo.checkin('cde-package')
