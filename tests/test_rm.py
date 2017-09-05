from __future__ import absolute_import

from nose.tools import *

import testit


class TestRm(testit.LocalCase):
    def test_all(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('rm')
            assert_equals(r.error_code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('rm', '-x')
            assert_equals(r.error_code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('rm', 'e1')
            assert_equals(r.error_code, 1)

        testit.sciunit('create', 'ok')
        assert_is_none(testit.sciunit('rm', 'e1'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('rm', 'e0')
            assert_equals(r.error_code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('rm', 'wat')
            assert_equals(r.error_code, 1)

        testit.sciunit('exec', 'pwd')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
            assert_equals(r.error_code, 0)

        assert_is_none(testit.sciunit('rm', 'e1'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
            assert_equals(r.error_code, 1)

        assert_is_none(testit.sciunit('exec', 'true'))
