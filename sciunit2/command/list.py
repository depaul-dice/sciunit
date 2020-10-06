from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
from sciunit2.util import quoted
from sciunit2 import timestamp
import sciunit2.workspace

from getopt import getopt


class ListCommand(AbstractCommand):
    name = 'list'

    @property
    def usage(self):
        return [('list', 'List executions in the sciunit')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if args:
            raise CommandLineError
        emgr, _ = sciunit2.workspace.current()
        entries = run_listing(emgr)
        if entries == 0:
            self.none()

    def none(self):
        print("Sciunit Empty\n")


def run_listing(emgr):
    counter = 0
    for rev, d in emgr.list():
        print('%5s %s %s' % (
            rev,
            timestamp.fmt_ls(d.started),
            quoted(d.cmd)))
        ++counter
    return counter
