import logging

logger = logging.getLogger(__name__)


def get_first_field(obj, field_name, attribute_name='value', default=''):
    try:
        return obj[field_name]['und'][0][attribute_name].strip() or default
    except:
        return default


def get_field_attributes(json_object, field_name, attribute_name='value', default=None):
    if default is None:
        default = []
    try:
        return [obj[attribute_name].strip() for obj in json_object[field_name]['und']]
    except:
        return default


def get_field(obj, field_name, default=''):
    try:
        return obj[field_name]['und'] or default
    except:
        return default