from __future__ import absolute_import

from unittest import mock
import unittest
import os
import shutil

import sciunit2.cli
import sciunit2.workspace

# these are important packages, used through arguments
from humanfriendly.testing import touch, CaptureOutput
from humanfriendly.testing import make_dirs as mkdir


class LocalCase(unittest.TestCase):
    def setUp(self):
        self.workspace_patch = mock.patch(
            'sciunit2.workspace.location_for',
            lambda s: os.path.join('tmp', s))
        self.workspace_patch.start()

    def tearDown(self):
        self.workspace_patch.stop()
        shutil.rmtree('tmp', True)


def sciunit(*args):
    with mock.patch('sys.argv', ['x'] + list(args)):
        sciunit2.cli.main()
