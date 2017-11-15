from __future__ import absolute_import

from sciunit2.exceptions import CommandError
from sciunit2.util import quoted_format, quoted, Chdir
import sciunit2.libexec

import os
import shutil
import shlex
import json
import subprocess


def capture(args):
    sciunit2.libexec.ptu(args).wait()
    assert os.path.isdir('cde-package')
    with open('cde-package/cde.log', 'r+') as f:
        content = f.read()
        f.seek(0)
        write_cmd(f, args)
        f.write(content)


def shell():
    print 'Interactive capturing started; press Ctrl-D to end'
    sciunit2.libexec.ptu([sciunit2.libexec.scripter.which,
                          '-qi', 'cde.stdin']).wait()
    assert os.path.isdir('cde-package')
    print 'Interactive capturing ended'
    shutil.move('cde.stdin', 'cde-package')
    with open('cde-package/cde.log') as f:
        ls = shlex.split(f, comments=True)
    with open('cde-package/cde.log', 'w') as f:
        f.write(quoted_format('{0} {1}\n', ls[0], ls[1]))
        f.write(quoted_format('{0} -qi /dev/null < {1}\n',
                              ls[2], os.path.relpath('cde.stdin', ls[1])))


def repeat(pkgdir, orig, newargs):
    if newargs:
        if not orig:
            raise CommandError(
                "interactive sciunit doesn't react to arguments")
        with Chdir(pkgdir):
            with open('cde.log') as f:
                ls = shlex.split(f, comments=True)
            os.rename('cde.log', 'cde.log.1')
            with open('cde.log', 'w') as f:
                write_cmd(f, orig[:1] + newargs)
                f.write(quoted_format('{0} {1}\n', ls[0], ls[1]))
                print >> f, quoted([ls[2]] + newargs)

    return subprocess.call(['/bin/sh', 'cde.log'], cwd=pkgdir)


def write_cmd(fp, args):
    fp.write('# ')
    json.dump(args, fp)
    fp.write('\n')


def read_cmd(fp):
    ln = fp.readline()
    if ln.startswith('# ['):
        return json.loads(ln[2:])
    else:
        return []
