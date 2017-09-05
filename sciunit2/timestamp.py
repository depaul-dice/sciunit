from __future__ import absolute_import

from utcdatetime import utcdatetime
from datetime import datetime as _datetime
import tzlocal


now = utcdatetime.now
fromstring = utcdatetime.from_string


def localized(dt):
    return dt.astimezone(tzlocal.get_localzone())


def fmt_ls(dt):
    dt = localized(dt)
    return (dt.strftime('%b %-2d %H:%M')
            if dt.year == _datetime.today().year
            else dt.strftime('%b %-2d %-5Y'))


def fmt_iso(dt):
    dt = localized(dt)
    return dt.strftime('%Y-%m-%d %H:%M')
