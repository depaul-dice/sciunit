from __future__ import absolute_import

import os
import pipes
import tempfile
import itertools
import errno


def quoted_format(fmt, *args):
    return fmt.format(*map(pipes.quote, args))


def quoted(args):
    return ' '.join(map(pipes.quote, args))


def _temp_names_derivedfrom(base, sep):
    yield base
    names = tempfile._get_candidate_names()
    for name in itertools.islice(names, 0, tempfile.TMP_MAX):
        yield base + sep + name


def mkdir_derivedfrom(base, sep, mode=0777):
    base = os.path.normpath(base)

    for p in _temp_names_derivedfrom(base, sep):
        try:
            os.mkdir(p, mode)
            return p
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                continue
            raise  # pragma: no cover

    raise IOError(errno.EEXIST, "No usable temporary directory name found")


class Chdir(object):
    __slots__ = ['cwd', 'target']

    def __init__(self, target):
        self.cwd = os.getcwd()
        self.target = target

    def __enter__(self):
        os.chdir(self.target)
        return self

    def __exit__(self, *args):
        os.chdir(self.cwd)
