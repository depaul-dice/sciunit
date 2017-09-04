from __future__ import absolute_import

from nose.tools import *
import os

import testit
import sciunit2.archiver


class TestOpen(testit.LocalCase):
    def test_dir(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('open')
            assert_equals(r.error_code, 2)

        testit.sciunit('create', 'yes')
        assert_is_none(testit.sciunit('open', 'yes'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'a.xml')
            assert_equals(r.error_code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'nonexistent')
            assert_equals(r.error_code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', '-n')
            assert_equals(r.error_code, 2)

    def test_zip(self):
        testit.sciunit('create', 'yes')

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'nonexistent.zip')
            assert_equals(r.error_code, 1)

        assert_equals(sciunit2.archiver.make('tmp/yes'), 'tmp/yes.zip')

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'tmp/yes.zip')
            assert_equals(r.error_code, 1)

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
            assert_equals(r.error_code, 0)

        assert_is_none(testit.sciunit('open', 'yes'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
            assert_equals(r.error_code, 1)
