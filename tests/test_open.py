from __future__ import absolute_import

from nose.tools import *
import os

import testit
import sciunit2.archiver


class TestOpen(testit.LocalCase):
    def test_dir(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('open')
        assert_equals(r.exception.code, 2)

        testit.sciunit('create', 'yes')
        assert_is_none(testit.sciunit('open', 'yes'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'a.xml')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'nonexistent')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', '-n')
        assert_equals(r.exception.code, 2)

    def test_zip(self):
        testit.sciunit('create', 'yes')

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'nonexistent.zip')
        assert_equals(r.exception.code, 1)

        assert_equals(sciunit2.archiver.make('tmp/yes'), 'tmp/yes.zip')

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'tmp/yes.zip')
        assert_equals(r.exception.code, 1)

        testit.sciunit('exec', 'true')

        assert_equals(sciunit2.archiver.make('tmp/yes'), 'tmp/yes.zip')
        os.rename('tmp/yes.zip', 'tmp_x.zip')
        testit.sciunit('rm', 'e1')

        try:
            assert_is_none(testit.sciunit('open', './tmp_x.zip'))
        finally:
            os.unlink('tmp_x.zip')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 0)

        assert_is_none(testit.sciunit('open', 'yes'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 1)

    def test_rename(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('open', '-m')
        assert_equals(r.exception.code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', '-m', 'a', 'b')
        assert_equals(r.exception.code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', '-m', 'nowhere')
        assert_equals(r.exception.code, 1)

        testit.sciunit('create', 'empty')
        testit.sciunit('create', 'old')
        testit.sciunit('exec', 'true')

        assert_is_none(testit.sciunit('open', '-m', 'new'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'old')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 0)

        assert_is_none(testit.sciunit('open', '-m', 'empty'))
        assert_is_none(testit.sciunit('open', '-m', 'notempty'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'new')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r:
            testit.touch('tmp/new')
            testit.sciunit('open', '-m', 'new')
        assert_equals(r.exception.code, 1)

        testit.sciunit('create', 'empty')

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', '-m', 'notempty')
        assert_equals(r.exception.code, 1)
