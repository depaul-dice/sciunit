from __future__ import absolute_import

import shutil

from nose.tools import *

from tests import testit
import os


class TestExport(testit.LocalCase):
    def test_all(self):
        # with assert_raises(SystemExit) as r:
        #     testit.sciunit('export')
        # assert_equal(r.exception.code, 2)
        testit.sciunit('create', 'ok')
        testit.sciunit('exec', 'python', 'cwd.py')
        testit.sciunit('export', 'e1')
        req_file = 'e1-'+'requirements.txt'
        assert_true(os.path.isfile(req_file))
        os.remove(req_file)
