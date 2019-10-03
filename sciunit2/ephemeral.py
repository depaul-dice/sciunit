from __future__ import absolute_import

from urllib2 import HTTPError
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
from retry import retry
from contextlib import closing
import json
import tempfile
import shutil

register_openers()


def live(fn):
    with open(fn, 'rb') as f:
        datagen, headers = multipart_encode({"file": f})
        req = urllib2.Request("https://file.io/?expires=1d", datagen, headers)
        with closing(urllib2.urlopen(req)) as resp:
            return json.load(resp)['key'] + '#'


@retry(HTTPError, tries=3, delay=0.3, backoff=2)
def _download(token):
    return urllib2.urlopen("https://file.io/" + token)


def fetch(token, base):
    with closing(_download(token)) as resp:
        f = tempfile.NamedTemporaryFile(prefix=base, dir='')
        shutil.copyfileobj(resp, f)
        f.seek(0)
        return f
