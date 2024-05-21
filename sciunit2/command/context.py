from __future__ import absolute_import

import sciunit2.workspace

from contextlib import contextmanager
import os

import shutil
import time

from getopt import getopt
import sys
import fcntl

class FileLock:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_handle = None

    def acquire(self):
        self.file_handle = open(self.file_path, 'w')
        fcntl.flock(self.file_handle, fcntl.LOCK_EX)

    def release(self):
        if self.file_handle:
            fcntl.flock(self.file_handle, fcntl.LOCK_UN)
            self.file_handle.close()

# returns the pkgdir and original command used
# to execute execution 'rev'
@contextmanager
def CheckoutContext(rev):
    lock = FileLock('lockfile')
    lock.acquire()
    emgr, repo = sciunit2.workspace.current()
    try:
        with emgr.exclusive():
            orig = emgr.get(rev).cmd
            pkgdir = os.path.join(repo.location, 'cde-package')
            pkgdir_rev = os.path.join(repo.location, rev, 'cde-package')
            repo.cleanup(pkgdir)
            repo.cleanup(pkgdir_rev)
            repo.checkout(rev)
            shutil.copytree(pkgdir, pkgdir_rev)
            yield pkgdir_rev, orig
    finally:
        lock.release()


@contextmanager
def CheckoutContext_Diff(rev):
    emgr, repo = sciunit2.workspace.current()
    with emgr.exclusive():
        orig = emgr.get(rev).cmd
        pkgdir = os.path.join(repo.location, 'cde-package' + rev)
        repo.cleanup(pkgdir)
        repo.checkout(rev)
        yield pkgdir, orig
