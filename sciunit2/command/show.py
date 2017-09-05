from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError, CommandError
from sciunit2.records import DBNotFoundError
from sciunit2.util import quoted
from sciunit2 import timestamp
import sciunit2.workspace

from getopt import getopt
import sys
import humanfriendly


class ShowCommand(AbstractCommand):
    name = 'show'

    @property
    def usage(self):
        return [('show [<execution id>]',
                 'Show detailed information of an execution')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if len(args) > 1:
            raise CommandLineError

        emgr, repo = sciunit2.workspace.current()
        name = _remove_prefix_if_presents(
            repo.location, sciunit2.workspace.location_for(''))
        if args:
            rev = args[0]
            e = emgr.get(rev)
        else:
            try:
                rev, e = emgr.last()
            except DBNotFoundError:
                raise CommandError('sciunit %r is empty' % name)

        ls = [('id', rev),
              ('sciunit', name),
              ('command', quoted(e.cmd)),
              ('size', humanfriendly.format_size(e.size)),
              ('started', timestamp.fmt_iso(e.started))]
        for ln in ls:
            sys.stdout.write('%7s: %s\n' % ln)


def _remove_prefix_if_presents(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s