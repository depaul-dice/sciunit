from __future__ import absolute_import

from nose.tools import *
import os

import testit


class TestCreate(testit.LocalCase):
    def test_all(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('create')
        assert_equals(r.exception.code, 2)

        testit.sciunit('create', 'ok')
        assert_true(os.path.isdir('tmp/ok'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('create', 'ok')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('create', 'a.zip')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r:
            open('tmp/notok', 'w').close()
            testit.sciunit('create', 'notok')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('create', '-h')
        assert_equals(r.exception.code, 2)
