from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.command.context import CheckoutContext
from sciunit2.exceptions import CommandLineError
import sciunit2.core

from getopt import getopt
import sys


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
        with CheckoutContext(args[0]) as (pkgdir, orig):
            returnValue = sciunit2.core.repeat(pkgdir, orig, args[1:])
        if returnValue != 0:
            sys.exit(returnValue)

        return args

    def note(self, data):
        return "repeated execution {0}\n".format(
            data[0])
