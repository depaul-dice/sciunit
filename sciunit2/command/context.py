from __future__ import absolute_import

import sciunit2.workspace

from contextlib import contextmanager
import os


@contextmanager
def CheckoutContext(rev):
    emgr, repo = sciunit2.workspace.current()
    with emgr.exclusive():
        orig = emgr.get(rev).cmd
        pkgdir = os.path.join(repo.location, 'cde-package')
        repo.cleanup(pkgdir)
        repo.checkout(rev)
        yield (pkgdir, orig)
