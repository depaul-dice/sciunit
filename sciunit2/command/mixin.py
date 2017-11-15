from __future__ import absolute_import

from sciunit2.util import quoted
from sciunit2.cdelog import open
from sciunit2 import timestamp
import sciunit2.workspace

from humanfriendly import Spinner
import os
import errno


class CommitMixin(object):
    def do_commit(self, rev, emgr, repo, dir=''):
        with Spinner('Committing') as sp:
            sz = repo.checkin(rev, os.path.join(dir, 'cde-package'), sp)
        return (repo.location,) + emgr.commit(sz)

    def do_getcmd(self, dir=''):
        try:
            with open(os.path.join(dir, 'cde-package/cde.log')) as f:
                ls = f.read_cmd()
            yield ls
        except IOError as exc:
            if exc.errno != errno.ENOENT:
                raise  # pragma: no cover

    def note(self, (p, rev, d)):
        return "\n[%s %s] %s\n Date: %s\n" % (
            sciunit2.workspace.project(p),
            rev,
            quoted(d.cmd),
            timestamp.fmt_rfc2822(d.started))
