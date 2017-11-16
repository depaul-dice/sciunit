from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.command.mixin import CommitMixin
from sciunit2.exceptions import CommandLineError
import sciunit2.core
import sciunit2.workspace

from getopt import getopt


class ExecCommand(CommitMixin, AbstractCommand):
    name = 'exec'

    @property
    def usage(self):
        return [('exec <executable> [<args...>]',
                 'Capture an execution of the given command line'),
                ('exec -i',
                 "Capture user's interactions inside a shell")]

    def run(self, args):
        optlist, args = getopt(args, 'i')
        if bool(optlist) == bool(args):
            raise CommandLineError
        emgr, repo = sciunit2.workspace.current()
        with emgr.exclusive():
            rev = emgr.add(args)
            if optlist:
                sciunit2.core.shell()
            else:
                sciunit2.core.capture(args)
            return self.do_commit('cde-package', rev, emgr, repo)
