from __future__ import absolute_import

from nose.tools import *
import os
import mock
import ddt
import pwd
import re

import testit


patch_tilde = mock.patch('os.path.expanduser',
                         lambda x: x.replace('~/', 'tmp/'))


@ddt.ddt
class TestGiven(testit.LocalCase):
    @ddt.data('/usr/local/bash', '/bin/tcsh', '/opt/bin/fish')
    @patch_tilde
    def test_all(self, shell):
        def mock_getpwuid(uid):
            return pwd.struct_passwd(['', '', '', '', '', '', shell])

        testit.mkdir('tmp')

        with mock.patch('pwd.getpwuid', mock_getpwuid):
            with assert_raises(SystemExit) as r:
                testit.sciunit('post-install', '-x')
            assert_equals(r.exception.code, 2)

            with testit.CaptureOutput() as out:
                testit.sciunit('post-install')

            if not out.getvalue():
                return

            assert_true(out.getvalue().startswith('x '))

            p = os.path.expanduser(out.getvalue().rstrip()[2:])
            assert_true(os.path.isfile(p))

            with open(p) as fp:
                content = fp.read()

            with testit.CaptureOutput() as out:
                testit.sciunit('post-install')

            with open(p) as fp:
                assert_equals(fp.read(), content)

            a = 'echo "old code"\n'
            b = 'more code\n'
            with open(p, 'w') as fp:
                fp.write(a)
                fp.write(content)
                fp.write(b)

            with testit.CaptureOutput() as out:
                testit.sciunit('post-install')

            with open(p) as fp:
                assert_equals(fp.read(), a + content + b)

            os.unlink(p)
            os.mkdir(p)

            with testit.CaptureOutput() as out:
                testit.sciunit('post-install')

            patch_tilde.stop()
            po = re.search(r'^\s*(~/[^\n]*)$', out.getvalue(), re.M).group(1)
            assert_true(os.path.isfile(os.path.expanduser(po)))
            patch_tilde.start()
