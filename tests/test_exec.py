from __future__ import absolute_import

from nose.tools import *

import testit


class TestExec(testit.LocalCase):
    def test_cli(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('exec')
            assert_equals(r.error_code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('exec', '-i', 'x')
            assert_equals(r.error_code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('exec', 'pwd')
            assert_equals(r.error_code, 1)

        testit.sciunit('create', 'ok')
        assert_is_none(testit.sciunit('exec', 'pwd'))

        open('tmp/ok/e2.json', 'w').close()

        with assert_raises(SystemExit) as r:
            testit.sciunit('exec', 'pwd')
            assert_equals(r.error_code, 1)
