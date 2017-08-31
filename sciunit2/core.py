from __future__ import absolute_import

import sciunit2.libexec
from sciunit2.util import quoted_format

import os
import shutil
import shlex


def capture(args):
    sciunit2.libexec.ptu(args).wait()
    assert os.path.isdir('cde-package')


def shell():
    sciunit2.libexec.ptu([sciunit2.libexec.scripter.location,
                          '-i', 'cde.stdin']).wait()
    assert os.path.isdir('cde-package')
    shutil.move('cde.stdin', 'cde-package')
    with open('cde-package/cde.log') as f:
        ls = shlex.split(f)
    with open('cde-package/cde.log', 'w') as f:
        f.write(quoted_format('{0} {1}\n', ls[0], ls[1]))
        f.write(quoted_format('{0} -qi /dev/null < {1}\n',
                              ls[2], os.path.relpath('cde.stdin', ls[1])))
