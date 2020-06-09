from __future__ import absolute_import

import urllib.request
import urllib.error
import requests

from retry import retry
from contextlib import closing
import tempfile
import shutil


def live(fn):
    with open(fn, 'rb') as f:
        with closing(requests.post("https://file.io/?expires=1d",
                                   files={"file": f})) as resp:
            return resp.json()['key'] + '#'


@retry(urllib.error.HTTPError, tries=3, delay=0.3, backoff=2)
def _download(token):
    return urllib.request.urlopen("https://file.io/" + token)


def fetch(token, base):
    with closing(_download(token)) as resp:
        f = tempfile.NamedTemporaryFile(prefix=base, dir='')
        shutil.copyfileobj(resp, f)
        f.seek(0)
        return f
