from __future__ import absolute_import
import __builtin__

from sciunit2.exceptions import CommandError
import sciunit2.version_control

import os
import re
import pipes
import errno


def _mkdir_p(path):
    try:
        os.makedirs(path)
        return True
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            return False
        else:
            raise


def _is_path_component(s):
    return re.match(r'^[\w -]+$', s)


def location_for(name):
    return os.path.expanduser('~/sciunit/%s' % name)


def create(name):
    if not _is_path_component(name):
        raise CommandError('%r contains disallowed characters' % name)

    if not _mkdir_p(location_for(name)):
        raise CommandError('directory %s already exists' %
                           location_for(pipes.quote(name)))


def open(s):
    if os.path.isdir(location_for(s)):
        with __builtin__.open(location_for('.activated'), 'w') as f:
            print >> f, s
    else:
        raise CommandError('sciunit %r not found' % s)


def repo():
    try:
        with __builtin__.open(location_for('.activated')) as f:
            ln = f.readline()
            assert ln[-1] == '\n'
            p = location_for(ln[:-1])
            os.stat(p)
            return sciunit2.version_control.Vvpkg(p)

    except (OSError, IOError):
        raise CommandError('no opened sciunit')
