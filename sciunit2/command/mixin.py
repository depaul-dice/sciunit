from __future__ import absolute_import

from sciunit2.util import quoted
from sciunit2.cdelog import open
from sciunit2 import timestamp
import sciunit2.workspace

from humanfriendly import Spinner


class CommitMixin(object):
    def do_commit(self, pkgdir, rev, emgr, repo):
        with Spinner('Committing') as sp:
            sz = repo.checkin(rev, pkgdir, sp)
        return (repo.location,) + emgr.commit(sz)

    def note(self, (p, rev, d)):
        return "\n[%s %s] %s\n Date: %s\n" % (
            sciunit2.workspace.project(p),
            rev,
            quoted(d.cmd),
            timestamp.fmt_rfc2822(d.started))
