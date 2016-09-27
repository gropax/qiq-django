import pytz
from datetime import datetime


def age(date):
    delta = datetime.now(pytz.utc) - date
    years = delta.days // 365
    if years:
        return "%iy" % years
    weeks = delta.days // 7
    if weeks:
        return "%iw" % weeks
    if delta.days:
        return "%id" % delta.days
    hours = delta.seconds // 3600
    if hours:
        return "%ih" % hours
    minutes = delta.seconds // 60
    if minutes:
        return "%im" % minutes
    if delta.seconds:
        return "%is" % delta.seconds
    return ''
