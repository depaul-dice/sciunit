from __future__ import absolute_import

from sciunit2.exceptions import CommandError
from sciunit2.util import quoted_format, quoted, Chdir
import sciunit2.libexec

import os
import shutil
import shlex
import subprocess


def capture(args):
    sciunit2.libexec.ptu(args).wait()
    assert os.path.isdir('cde-package')


def shell():
    print 'Interactive capturing started; press Ctrl-D to end'
    sciunit2.libexec.ptu([sciunit2.libexec.scripter.which,
                          '-qi', 'cde.stdin']).wait()
    assert os.path.isdir('cde-package')
    print 'Interactive capturing ended'
    shutil.move('cde.stdin', 'cde-package')
    with open('cde-package/cde.log') as f:
        ls = shlex.split(f)
    with open('cde-package/cde.log', 'w') as f:
        f.write(quoted_format('{0} {1}\n', ls[0], ls[1]))
        f.write(quoted_format('{0} -qi /dev/null < {1}\n',
                              ls[2], os.path.relpath('cde.stdin', ls[1])))


def repeat(pkgdir, newargs):
    if newargs:
        with Chdir(pkgdir):
            if os.path.isfile('cde.stdin'):
                raise CommandError(
                    "interactive sciunit doesn't react to arguments")
            with open('cde.log') as f:
                ls = shlex.split(f)
            os.rename('cde.log', 'cde.log.1')
            with open('cde.log', 'w') as f:
                f.write(quoted_format('{0} {1}\n', ls[0], ls[1]))
                print >> f, quoted([ls[2]] + newargs)

    return subprocess.call(['/bin/sh', 'cde.log'], cwd=pkgdir)
