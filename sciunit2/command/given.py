#Note: Converted
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
from distutils.dir_util import create_tree, copy_tree, _path_created
from distutils.file_util import copy_file

from sciunit2.command.mixin import CommitMixin

#class GivenCommand(AbstractCommand):
class GivenCommand(CommitMixin, AbstractCommand):
    name = 'given'

    @property
    def usage(self):
        return [('given <glob> repeat <execution id> [<%|args...>]',
                 "Repeat <execution id> with additional files or directories "
                 "specified by <glob>")]

    def run(self, args): # args = <glob> repeat <execution id> %
        optlist, args = getopt(args, '') # args = <glob> repeat <execution id> %
        if len(args) < 3 or args[1] != 'repeat':
            raise CommandLineError
        files, args = globsub(args[0], args[2:])
        # files = list of files or dirs in <glob>
        # args = <execution id> list of args after % + files
        if not files:
            raise CommandError('no match')
        self.name = 'repeat'
        optlist, args = getopt(args, '')
        #print('Hai test: ')
        #print(args)

        with CheckoutContext(args[0]) as (pkgdir, orig):
            try:
                #pkgdir = /path/to/sciunit/currentproject/cde-package
                #print('pkgdir and orig')
                #print(pkgdir)
                #print(orig)
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
                    target = join_fn(dst, fn)
                    if os.path.isdir(fn):
                        copy_tree(fn, target)
                    else:
                        copy_file(fn, target)
                _path_created.clear()

            except DistutilsFileError as e:
                raise CommandError(e)
            else:
                #sys.exit(sciunit2.core.repeat(pkgdir, orig, args[1:]))
                sciunit2.core.repeat(pkgdir, orig, args[1:])
        emgr, repo = sciunit2.workspace.current()
        pkgdir = os.path.join(repo.location, 'cde-package')
        print(pkgdir)
        with emgr.exclusive():
            rev = emgr.add(args[1:])
            return self.do_commit(pkgdir, rev, emgr, repo)

    #def note(self, aList):
    #    return "\n %s \n %s \n" % (aList[0].decode('utf-8'), aList[1].decode('utf-8'))
