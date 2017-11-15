from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.command.mixin import CommitMixin
from sciunit2.exceptions import CommandLineError, CommandError
import sciunit2.workspace

from getopt import getopt


class CommitCommand(CommitMixin, AbstractCommand):
    name = 'commit'

    @property
    def usage(self):
        return [('commit', 'Commit the finishing state of the last repeat '
                           'command as a new execution')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if args:
            raise CommandLineError
        emgr, repo = sciunit2.workspace.current()
        with emgr.exclusive():
            for cmd in self.do_getcmd(repo.location):
                rev = emgr.add(cmd)
                return self.do_commit(rev, emgr, repo, dir=repo.location)
            else:
                raise CommandError('nothing to commit')
