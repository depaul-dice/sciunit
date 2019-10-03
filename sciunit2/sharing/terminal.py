from __future__ import absolute_import

from sciunit2.sharing import AbstractWizard

import readline
import sys
from tqdm import tqdm


class TerminalWizard(AbstractWizard):  # pragma: no cover
    def ask(self, msg, *args):
        ans = raw_input((msg + " [y/N] ") % args)
        return ans.strip() in 'yY'

    def prompt(self, msg, *args):
        return raw_input((msg + ' ') % args).strip()

    def info(self, msg, *args):
        print msg % args

    def progress(self, msg, nbytes):
        return tqdm(desc=msg, total=nbytes,
                    unit='B', unit_scale=True,
                    miniters=1)
