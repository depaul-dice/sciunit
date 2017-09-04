from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
import sciunit2.workspace

from getopt import getopt


class OpenCommand(AbstractCommand):
    name = 'open'

    @property
    def usage(self):
        return [('open <name>|<path to sciunit>.zip',
                 'Open the sciunit under ~/sciunit/<name>, or one in '
                 'a ZIP file by extracting it to a temporary directory')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if len(args) != 1:
            raise CommandLineError
        sciunit2.workspace.open(args[0])
