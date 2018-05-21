from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.command.context import CheckoutContext
from sciunit2.exceptions import CommandLineError
import sciunit2.core
import sciunit2.dakota

from getopt import getopt
import sys


class RepeatCommand(AbstractCommand):
    name = 'repeat'

    @property
    def usage(self):
        return [('repeat <execution id> [<args...>]',
                 "Repeat the execution of <execution id>"),
                ('repeat <path to dakota.in> [<args...>]',
                 "Repeat an execution in a Dakota analysis")]

    def run(self, args):
        optlist, args = getopt(args, '')
        if not args:
            raise CommandLineError
        if args[0].endswith('.in'):
            with sciunit2.dakota.RewroteInputFile(args[0]) as fin:
                with CheckoutContext(fin.eid) as (pkgdir, orig):
                    fin.prepare(pkgdir, orig)
                    sys.exit(sciunit2.dakota.run(fin.name, args[1:]))
        else:
            with CheckoutContext(args[0]) as (pkgdir, orig):
                sys.exit(sciunit2.core.repeat(pkgdir, orig, args[1:]))
