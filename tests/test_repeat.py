from __future__ import absolute_import

from nose.tools import *
import os

import testit


class TestRepeat(testit.LocalCase):
    def test_all(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat')
            assert_equals(r.error_code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', '-i')
            assert_equals(r.error_code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
            assert_equals(r.error_code, 1)

        testit.sciunit('create', 'ok')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'asdf')
            assert_equals(r.error_code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
            assert_equals(r.error_code, 1)

        testit.sciunit('exec', 'pwd')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
            assert_equals(r.error_code, 0)

        testit.sciunit('create', 'ok2')
        testit.sciunit('exec', 'pwd', '-x')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
            assert_equals(r.error_code, 2)

        testit.sciunit('open', 'ok')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
            assert_equals(r.error_code, 0)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1', '-x')
            assert_equals(r.error_code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1', '-L', '-P')
            assert_equals(r.error_code, 0)

        testit.sciunit('open', 'ok')
        # XXX Ctrl-D
        assert_is_none(testit.sciunit('exec', '-i'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e2')
            assert_equals(r.error_code, 0)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e2', '-l')
            assert_equals(r.error_code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
            assert_equals(r.error_code, 2)

        os.unlink('tmp/ok/e2.json')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e2')
            assert_equals(r.error_code, 1)
