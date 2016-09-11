import datetime
import json

from django.http import HttpResponse


def _custom_encoder(obj):
    """
    Serialize dates to ISO format: yyyy-mm-dd for dates and
    yyyy-mm-ddThh:mm:ss.xxxxxx for datetimes.
    """
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError('Not JSON serializable: %r' % obj)

default_json_encoder = json.JSONEncoder(default=_custom_encoder)


def to_json(value):
    """
    Accepts a dict and parses it as a JSON object
    :param value: the value to parse
    :return: {json}
    """
    return default_json_encoder.encode(value)


def json_response(data):
    """
    Accepts a json object and adds it to an HTTP response
    :param data: the json object to add to the payload
    :return: {HttpResponse}
    """
    return HttpResponse(to_json(data), content_type='application/json')