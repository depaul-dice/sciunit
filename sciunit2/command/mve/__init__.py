from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
from sciunit2 import workspace

from getopt import getopt
import re

from sciunit_convert.tree import Tree, save_tree
from sciunit_convert.nbrunner import tree_update, TREE_FILE

from .replay_order import replay_sequence
from .replay import replay


class MveCommand(AbstractCommand):
    name = 'mve'

    @property
    def usage(self):
        return [('mve e[m1]-e[n1],e[n2],e[m3]-e[n3],... <Cache Size>',
                 "Create a tree using given executions and cache size")]

    def run(self, args):
        optlist, args = getopt(args, 'v')
        verbose = False
        for o, _ in optlist:
            if o in ['-v']:
                verbose = True
        if not args or len(args) != 2:
            raise CommandLineError
        execs = set()
        for a in args[0].split(','):
            match = re.match(r'e(\d+)(?:\-e(\d+))?', a)
            if not match:
                raise CommandLineError
            if match[2] is not None:
                execs.update(range(int(match[1]), int(match[2]) + 1))
            else:
                execs.add(match[1])
        t = Tree()
        for i in execs:
            tree_update(t, i, f'{workspace.current()[1].location}/e{i}.bin')
        save_tree(t, TREE_FILE)
        replay_sequence(TREE_FILE, int(args[1]), 'ro.bin')
        replay('ro.bin', verbose)
