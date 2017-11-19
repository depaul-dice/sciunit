from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.command.context import CheckoutContext
from sciunit2.exceptions import CommandLineError, CommandError
from sciunit2.util import globsub
from sciunit2.cdelog import open, DetachedExecution
import sciunit2.core

from getopt import getopt
import sys
import os
from distutils.errors import DistutilsFileError
from distutils.dir_util import create_tree
from distutils.file_util import copy_file


class GivenCommand(AbstractCommand):
    name = 'given'

    @property
    def usage(self):
        return [('given <glob> repeat <execution id> [<%|args...>]',
                 "Repeat <execution id> with additional files specified "
                 "by <glob>")]

    def run(self, args):
        optlist, args = getopt(args, '')
        if len(args) < 3 or args[1] != 'repeat':
            raise CommandLineError
        files, args = globsub(args[0], args[2:])
        if not files:
            raise CommandError('no match')
        self.name = 'repeat'
        optlist, args = getopt(args, '')

        with CheckoutContext(args[0]) as (pkgdir, orig):
            try:
                de = DetachedExecution(pkgdir)
                if os.path.isabs(files[0]):
                    dst = de.root_on_host()
                    create_tree(dst, (os.path.relpath(p, '/') for p in files))
                    join_fn = str.__add__
                else:
                    dst = de.cwd_on_host()
                    create_tree(dst, files)
                    join_fn = os.path.join

                for fn in files:
                    copy_file(fn, join_fn(dst, fn))

            except DistutilsFileError as e:
                raise CommandError(e)
            else:
                sys.exit(sciunit2.core.repeat(pkgdir, orig, args[1:]))
