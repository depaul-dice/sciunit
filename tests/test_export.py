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
        testit.sciunit('exec', 'python', 'export_example.py')
        eid = 'e1'
        testit.sciunit('export', eid)
        req_file = eid+'-requirements.txt'
        assert_true(os.path.isfile(req_file))
        os.remove(req_file)

        testit.sciunit('export', eid, 'virtualenv')
        data_dir = 'ok-'+eid
        env_dir = 'sciunit_env'
        assert_true(os.path.isfile(req_file))
        assert_true(os.path.isdir(env_dir))
        assert_true(os.path.isdir(data_dir))
        os.remove(req_file)
        shutil.rmtree(data_dir)
        shutil.rmtree(env_dir)
