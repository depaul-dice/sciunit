from __future__ import absolute_import
import __builtin__

from sciunit2.exceptions import CommandError
import sciunit2.version_control
import sciunit2.records
import sciunit2.archiver

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
    if s.endswith('.zip'):
        try:
            p = sciunit2.archiver.extract(s, _is_path_component, location_for)
        except sciunit2.archiver.BadZipfile as exc:
            raise CommandError(exc.message)
        else:
            _saved_opened(p)
    elif _is_path_component(s):
        path = location_for(s)
        if os.path.isdir(path):
            _saved_opened(path)
        else:
            raise CommandError('sciunit %r not found' % s)
    else:
        raise CommandError('unrecognized source')


def _saved_opened(path):
    with __builtin__.open(location_for('.activated'), 'w') as f:
        print >> f, path


def at():
    try:
        with __builtin__.open(location_for('.activated')) as f:
            ln = f.readline()
            assert ln[-1] == '\n'
            p = ln[:-1]
            os.stat(p)
            return p

    except (OSError, IOError):
        raise CommandError('no opened sciunit')


def current():
    p = at()
    return (sciunit2.records.ExecutionManager(p),
            sciunit2.version_control.Vvpkg(p))
