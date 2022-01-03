from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError

from getopt import getopt
import json

from sciunit_convert.convert import add_hooks, j2p


class ConvertCommand(AbstractCommand):
    name = 'convert'

    @property
    def usage(self):
        return [('convert <.ipynb>',
                 "Convert a Jupyter Notebook to a Python file for running using CHEX")]

    def run(self, args):
        optlist, args = getopt(args, '')
        if not args or len(args) != 1:
            raise CommandLineError
        with open(args[0], 'r', encoding='utf-8') as infile:
            notebook = json.load(infile)
        add_hooks(notebook)
        j2p(notebook, f'{args[0]}.py')
