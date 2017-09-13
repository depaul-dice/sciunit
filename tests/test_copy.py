from __future__ import absolute_import

from nose.tools import *
import mock
from cStringIO import StringIO

import testit


class TestCopy(testit.LocalCase):
    def test_all(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('copy', '-x')
        assert_equals(r.exception.code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('copy', 'x')
        assert_equals(r.exception.code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('copy')
        assert_equals(r.exception.code, 1)

        testit.sciunit('create', 'ok')
        testit.sciunit('exec', 'pwd')

        with assert_raises(SystemExit) as r:
            testit.sciunit('open', 'nonexistent#')
        assert_equals(r.exception.code, 1)

        out = StringIO()
        with mock.patch('sys.stdout', out):
            testit.sciunit('copy')
        token = out.getvalue().strip()

        assert_is_none(testit.sciunit('open', token))

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 0)

        out = StringIO()
        with mock.patch('sys.stdout', out):
            testit.sciunit('copy', '-n')
        path = out.getvalue().strip()

        assert_true(path.endswith('.zip'))
        assert_is_none(testit.sciunit('open', path))

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 0)
