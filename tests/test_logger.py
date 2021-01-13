from __future__ import absolute_import

from tests import testit
import sciunit2.logger


class TestLogger(testit.LocalCase):
    def test_all(self):
        self.assertEqual(sciunit2.logger.runlog("ERROR", "test", "testing logger", __file__), 1)  # test runlogat
        self.assertEqual(sciunit2.logger.runlog("WARNING", "test", "testing logger", __file__), 1)
        self.assertEqual(sciunit2.logger.runlog("INFO", "test", "testing logger", __file__), 1)

        testit.sciunit('create', 'ok')

        self.assertEqual(sciunit2.logger.runlog("ERROR", "test", "testing logger", __file__), 0)  # test runlog
        self.assertEqual(sciunit2.logger.runlog("WARNING", "test", "testing logger", __file__), 0)
        self.assertEqual(sciunit2.logger.runlog("INFO", "test", "testing logger", __file__), 0)

        self.assertEqual(sciunit2.logger.getpath(__file__), "tests/test_logger.py")  # test getpath
        self.assertEqual(sciunit2.logger.getpath("/sciunit2-python3/sciunit2/test.py"), "sciunit2/test.py")
