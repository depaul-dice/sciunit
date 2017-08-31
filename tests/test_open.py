from __future__ import absolute_import

from nose.tools import *
import os

import testit


class TestOpen(testit.LocalCase):
    def test_all(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('open')
            assert_equals(r.error_code, 2)

        testit.sciunit('create', 'yes')
        assert_is_none(testit.sciunit('open', 'yes'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'a.zip')
            assert_equals(r.error_code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'nonexistent')
            assert_equals(r.error_code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', '-n')
            assert_equals(r.error_code, 2)
