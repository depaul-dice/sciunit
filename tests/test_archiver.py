from __future__ import absolute_import

from nose.tools import *
import os
import shutil
import mock
import errno
import zipfile

import testit
import sciunit2.archiver


def prepare():
    os.makedirs('tmp/test')


def cleanup():
    shutil.rmtree('tmp', True)


@with_setup(prepare, cleanup)
def test_empty():
    p = sciunit2.archiver.make('tmp/test')
    assert_equals(p, 'tmp/test.zip')

    with assert_raises(sciunit2.archiver.BadZipfile):
        sciunit2.archiver.extract(p, lambda x: True, lambda x: x)


@with_setup(prepare, cleanup)
def test_layout():
    testit.touch('tmp/test/a.txt')
    testit.mkdir('tmp/test/b')

    p = sciunit2.archiver.make('tmp/test')

    with mock.patch('tempfile.TMP_MAX', 0):
        with assert_raises(IOError) as r:
            sciunit2.archiver.extract(
                p,
                lambda x: True,
                lambda x: os.path.join('tmp', x))
        assert_equals(r.exception.errno, errno.EEXIST)

    with zipfile.ZipFile(p, 'a') as f:
        f.write('tmp/test/a.txt', 'test/2nd/a.txt')

    assert_true(sciunit2.archiver.extract(
            p,
            lambda x: True,
            lambda x: os.path.join('tmp', x))
        .startswith(os.path.join('tmp', 'test__')))

    with zipfile.ZipFile(p, 'a') as f:
        f.write('tmp/test/a.txt')

    with assert_raises(sciunit2.archiver.BadZipfile):
        sciunit2.archiver.extract(p, lambda x: bool(x), lambda x: x)

    with zipfile.ZipFile(p, 'w') as f:
        f.write('tmp/test/a.txt', 'a.txt')

    with assert_raises(sciunit2.archiver.BadZipfile):
        sciunit2.archiver.extract(p, lambda x: bool(x), lambda x: x)
