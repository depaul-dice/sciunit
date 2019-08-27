#Note: Converted
# Note: import the poster 0.81 version ported to python3 (in Downloads directory)
from __future__ import absolute_import

#from urllib2 import HTTPError
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
#import urllib2
import urllib.request
import urllib.error
import requests

from retry import retry
from contextlib import closing
import json
import tempfile
import shutil

register_openers()


def live(fn):
    with open(fn, 'rb') as f:
        #datagen, headers = multipart_encode({"file": f})
        #req = urllib2.Request("https://file.io/?expires=1d", datagen, headers)
        #req = urllib.request("https://file.io/?expires=1d", datagen, headers)
        #req = requests("https://file.io/?expires=1d", files={"file": f})
        #with closing(urllib2.urlopen(req)) as resp:
        #with closing(urllib.request.urlopen("https://file.io/?expires=1d", files={"file": f})) as resp:
        with closing(requests.post("https://file.io/?expires=1d", files={"file": f})) as resp:
            #return json.load(resp)['key'] + '#'
            return resp.json()['key'] + '#'


@retry(urllib.error.HTTPError, tries=3, delay=0.3, backoff=2)
def _download(token):
    #return urllib2.urlopen("https://file.io/" + token)
    return urllib.request.urlopen("https://file.io/" + token)


def fetch(token, base):
    with closing(_download(token)) as resp:
        f = tempfile.NamedTemporaryFile(prefix=base, dir='')
        shutil.copyfileobj(resp, f)
        f.seek(0)
        return f
