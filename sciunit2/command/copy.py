from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
import sciunit2.workspace
import sciunit2.archiver
import sciunit2.ephemeral

from getopt import getopt


class CopyCommand(AbstractCommand):
    name = 'copy'

    @property
    def usage(self):
        return [('copy', 'Copy the sciunit and obtain a token for opening '
                         'it over the Internet')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if args:
            raise CommandLineError
        emgr, repo = sciunit2.workspace.current()
        with emgr.shared():
            fn = sciunit2.archiver.make(repo.location)
            print sciunit2.ephemeral.live(fn)
