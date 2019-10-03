#Note: Converted
from __future__ import absolute_import

from nose.tools import *
import shutil

import testit


class TestExec(testit.LocalCase):
    def test_cli(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('exec')
        assert_equals(r.exception.code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('exec', '-i', 'x')
        assert_equals(r.exception.code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('exec', 'pwd')
        assert_equals(r.exception.code, 1)

        testit.sciunit('create', 'ok')
        assert_is_none(testit.sciunit('exec', 'pwd'))

        testit.touch('tmp/ok/e2.json')

        with assert_raises(SystemExit) as r:
            testit.sciunit('exec', 'pwd')
        assert_equals(r.exception.code, 1)

        shutil.rmtree('cde-package', True)
