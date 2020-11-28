from __future__ import absolute_import
import builtins

from sciunit2.exceptions import CommandError
import sciunit2.version_control
import sciunit2.records
import sciunit2.archiver
import sciunit2.ephemeral
import sciunit2.wget
import sciunit2.logger

import os
import re
import pipes
import errno
from urllib.parse import urlparse
import urllib.request
import urllib.error


# acts like mkdir -p. Creates the complete
# directory tree if it does not exist
def _mkdir_p(path):
    try:
        os.makedirs(path)
        return True
    except OSError as exc:          #TODO: logging
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            return False
        else:
            sciunit2.logger.runlog("error", "_mkdir_p()", str(exc), "workspace.py")
            raise


def _try_rename(from_):
    def _inner(to):
        try:
            os.rename(from_, to)
            return True
        except OSError as exc: #TODO: logging
            if exc.errno == errno.ENOTEMPTY:
                return False
            else:
                sciunit2.logger.runlog("error", "_try_rename()", str(exc), "workspace.py")
                raise
    return _inner


# checks if 's' is a valid dir name
def _is_path_component(s):
    return re.match(r'^[\w -]+$', s)


def _is_once_token(s):
    return re.match(r'^[\w]+#$', s)


def location_for(name):
    return os.path.expanduser('~/sciunit/%s' % name)


def create(name):
    _create(name, _mkdir_p)


def rename(name):
    _create(name, _try_rename(at()))


# creates the given folder if does not exist
def _create(name, by):
    if not _is_path_component(name):
        sciunit2.logger.runlog("error", "create", '%r contains disallowed characters' % name, "workspace,py")
        raise CommandError('%r contains disallowed characters' % name)

    if not by(location_for(name)):
        sciunit2.logger.runlog("error", "create", 'directory %s already exists' %
                           pipes.quote(location_for(name)), "workspace,py")
        raise CommandError('directory %s already exists' %
                           pipes.quote(location_for(name)))


# opens a sciunit container already created
def open(s):
    _mkdir_p(location_for(''))  # makes sure that sciunit/ is present
    try:
        if urlparse(s).scheme:
            p = _extract(sciunit2.wget.fetch(s, location_for('wget-tmp')))
        elif s.endswith('.zip'):
            p = _extract(s)
        elif _is_once_token(s):
            p = _extract(sciunit2.ephemeral.fetch(s, location_for('tmp')))
        elif _is_path_component(s):
            p = location_for(s)
            if not os.path.isdir(p):
                sciunit2.logger.runlog("error", "open", 'sciunit %r not found' % s, "workspace.py")
                raise CommandError('sciunit %r not found' % s)
        else:
            sciunit2.logger.runlog("error", "open", 'unrecognized source', "workspace.py")
            raise CommandError('unrecognized source')

    except sciunit2.archiver.BadZipfile as exc:
        sciunit2.logger.runlog("error", "open", exc, "workspace.py")
        raise CommandError(exc)

    except urllib.error.HTTPError as exc:
        sciunit2.logger.runlog("error", "open", '%d %s' % (exc.code, exc.msg), "workspace.py")
        raise CommandError('%d %s' % (exc.code, exc.msg))

    else:
        _save_opened(p)
        return p


def _save_opened(path):
    with builtins.open(location_for('.activated'), 'w') as f:
        print(path, file=f)


# extracts contents of zip file 'fn' and
# returns in a dir
def _extract(fn):
    return sciunit2.archiver.extract(fn, _is_path_component, location_for)


# returns the location of .activated file in ~/sciunit
# .activated file contains the name of the currently
# active sciunit project
def at():
    try:
        with builtins.open(location_for('.activated')) as f:
            ln = f.readline()
            assert ln.endswith('\n')
            p = ln[:-1]
            os.stat(p)
            return p

    except (OSError, IOError):
        sciunit2.logger.runlogat("error", "at()", "CommandError: no opened sciunit", "workspace.py")
        raise CommandError('no opened sciunit')


def current():
    p = at()   # returns directory of the active sciunit project
    creat_Diff_repo()
    return (sciunit2.records.ExecutionManager(p),
            sciunit2.version_control.Vvpkg(p))


def creat_Diff_repo():
    p = at()
    p = os.path.join(p, 'Diff')
    _mkdir_p(p)
    return p


def project(p):
    return _remove_prefix_if_present(p, location_for(''))


def _remove_prefix_if_present(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s
