from __future__ import absolute_import

from nose.tools import *
import mock
from cStringIO import StringIO

import testit


class TestStage(testit.LocalCase):
    def test_g(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('stage', '-x')
        assert_equals(r.exception.code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('stage', 'x')
        assert_equals(r.exception.code, 2)

        testit.sciunit('create', 'ok')
        testit.sciunit('exec', 'true')

        out = StringIO()
        with mock.patch('sys.stdout', out):
            testit.sciunit('stage', '-g')
        path = out.getvalue().strip()

        assert_true(path.endswith('.zip'))
        assert_is_none(testit.sciunit('open', path))

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 0)
