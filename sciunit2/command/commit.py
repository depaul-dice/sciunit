# Note: Converted
from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.command.mixin import CommitMixin
from sciunit2.exceptions import CommandLineError, CommandError
from sciunit2.cdelog import DetachedExecution
import sciunit2.workspace
import sciunit2.logger

from getopt import getopt
import os


class CommitCommand(CommitMixin, AbstractCommand):
    name = 'commit'

    @property
    def usage(self):
        return [('commit', 'Commit the finishing state of the last repeat '
                           'command as a new execution')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if args:
            sciunit2.logger.runlog("ERROR", "commit",
                                   "CommandLineError: no arguments expected", __file__)
            raise CommandLineError
        emgr, repo = sciunit2.workspace.current()  # repo is vvpkg
        pkgdir = os.path.join(repo.location, 'cde-package')
        with emgr.exclusive():
            for cmd in DetachedExecution(pkgdir).getcmd():
                rev = emgr.add(cmd)
                return self.do_commit(pkgdir, rev, emgr, repo)
            else:
                sciunit2.logger.runlog("ERROR", "commit",
                                       "CommandError: nothing to commit", __file__)
                raise CommandError('nothing to commit')

    def note(self, data):
        return "committed execution {0} in sciunit {1}\n".format(
            data[1], data[0])
