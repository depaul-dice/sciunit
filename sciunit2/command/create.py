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
        return [('create <name> [-f]',
                 'Create and open a new sciunit under ~/sciunit/<name>.\n'
                 'The -f flag overwrites the existing directory.')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if len(args) == 1:
            sciunit2.workspace.create(args[0].strip())
        elif len(args) == 2:
            flag = args[1]
            if flag != '-f':
                raise CommandLineError
            else:
                print('Warning: This will overwrite existing sciunit!')
                sciunit2.workspace.create(args[0].strip(), overwrite=True)
        else:
            raise CommandLineError
        return sciunit2.workspace.open(args[0])

    def note(self, project_dir):
        return quoted_format('Opened empty sciunit at {0}\n', project_dir)
