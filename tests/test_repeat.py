from __future__ import absolute_import

from nose.tools import *
import os
import testpath

import testit


class TestRepeat(testit.LocalCase):
    def test_all(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat')
        assert_equals(r.exception.code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', '-i')
        assert_equals(r.exception.code, 2)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 1)

        testit.sciunit('create', 'ok')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'asdf')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 1)

        testit.sciunit('exec', 'pwd')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 0)

        testit.sciunit('create', 'ok2')
        testit.sciunit('exec', 'sh', '-c', 'exit 3')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 3)

        testit.sciunit('open', 'ok')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 0)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1', '-x')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1', '-L', '-P')
        assert_equals(r.exception.code, 0)

        testit.sciunit('open', 'ok')
        with testpath.modified_env({'SHELL': '/bin/true'}):
            assert_is_none(testit.sciunit('exec', '-i'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e2')
        assert_equals(r.exception.code, 0)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e2', '-l')
        assert_equals(r.exception.code, 1)

        assert_is_none(testit.sciunit('commit'))

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e3')
        assert_equals(r.exception.code, 0)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1', '-L')
        assert_equals(r.exception.code, 0)

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e1')
        assert_equals(r.exception.code, 0)

        os.unlink('tmp/ok/e2.json')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'e2')
        assert_equals(r.exception.code, 1)

    def test_dakota(self):
        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'MANIFEST.in')
        assert_equals(r.exception.code, 1)

        testit.sciunit('create', 'ok')
        testit.sciunit('exec', '/bin/true')

        with assert_raises(SystemExit) as r:
            testit.sciunit('repeat', 'files/dakota_sample.in')
        assert_equals(r.exception.code, 1)

        with assert_raises(SystemExit) as r, testpath.assert_calls('dakota'):
            testit.sciunit('repeat', 'files/dakota_sample.in')
        assert_equals(r.exception.code, 0)
