from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
from sciunit2.util import quoted
from sciunit2 import timestamp
import sciunit2.core
import sciunit2.workspace

from getopt import getopt
from humanfriendly import Spinner


class ExecCommand(AbstractCommand):
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
            with Spinner('Committing') as sp:
                sz = repo.checkin(rev, 'cde-package', sp)
            return (repo.location,) + emgr.commit(sz)

    def note(self, (p, rev, d)):
        return "\n[%s %s] %s\n Date: %s\n" % (
            sciunit2.workspace.project(p),
            rev,
            quoted(d.cmd),
            timestamp.fmt_rfc2822(d.started))
