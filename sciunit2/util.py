from __future__ import absolute_import

import os
import pipes


def quoted_format(fmt, *args):
    return fmt.format(*map(pipes.quote, args))


def quoted(args):
    return ' '.join(map(pipes.quote, args))


class Chdir(object):
    __slots__ = ['cwd', 'target']

    def __init__(self, target):
        self.cwd = os.getcwd()
        self.target = target

    def __enter__(self):
        os.chdir(self.target)
        return self

    def __exit__(self, *args):
        os.chdir(self.cwd)
