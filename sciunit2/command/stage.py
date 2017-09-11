from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
import sciunit2.workspace
import sciunit2.archiver

from getopt import getopt


class StageCommand(AbstractCommand):
    name = 'stage'

    @property
    def usage(self):
        return [('stage -g', 'Generate ~/sciunit/<name>.zip only')]

    def run(self, args):
        optlist, args = getopt(args, 'g')
        if args or not optlist:
            raise CommandLineError
        emgr, repo = sciunit2.workspace.current()
        with emgr.shared():
            print sciunit2.archiver.make(repo.location)
