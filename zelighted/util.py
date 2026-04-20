import calendar
import datetime
import time

import tzlocal


def _encode_datetime(dttime):
    if (hasattr(dttime, 'tzinfo') and dttime.tzinfo and
            dttime.tzinfo.utcoffset(dttime) is not None):
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        if isinstance(dttime, datetime.date):
            dttime = naive_date_to_datetime(dttime)
        tz = tzlocal.get_localzone()
        if hasattr(tz, 'localize'):
            local_datetime = tz.localize(dttime)
        else:
            local_datetime = dttime.replace(tzinfo=tz)
        utc_timestamp = aware_datetime_to_epoch_seconds(local_datetime)

    return int(utc_timestamp)


def encode(data):
    for key, value in data.items():
        if value is None:
            continue
        elif isinstance(value, list) or isinstance(value, tuple):
            for subvalue in value:
                yield ("%s[]" % (key,), subvalue)
        elif isinstance(value, dict):
            subdict = dict(('%s[%s]' % (key, subkey), subvalue) for
                           subkey, subvalue in value.items())
            for subkey, subvalue in encode(subdict):
                yield (subkey, subvalue)
        elif (isinstance(value, datetime.datetime) or
              isinstance(value, datetime.date)):
            yield (key, _encode_datetime(value))
        else:
            yield (key, value)


def naive_date_to_datetime(naive_date):
    return datetime.datetime(*naive_date.timetuple()[:6])


def aware_datetime_to_epoch_seconds(localized_datetime):
    raw_seconds = time.mktime(localized_datetime.utctimetuple())
    epoch_seconds = time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))
    return raw_seconds - epoch_seconds
