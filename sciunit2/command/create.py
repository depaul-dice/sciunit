from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
from sciunit2.util import quoted_format
import sciunit2.workspace

from getopt import getopt


# this class creates a new sciunit project
# under ~/sciunit identified by <name>
class CreateCommand(AbstractCommand):
    name = 'create'

    @property
    def usage(self):
        return [('create <name>',
                 'Create and open a new sciunit under ~/sciunit/<name>')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if len(args) != 1:
            sciunit2.logger.runlog("error", "create", "CommandLineError", "create.py")
            raise CommandLineError
        sciunit2.workspace.create(args[0])
        return sciunit2.workspace.open(args[0])

    def note(self, project_dir):
        return "created and opened empty sciunit at {0}\n".format(
            project_dir)
