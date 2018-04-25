import hashlib


def key_value_sort_join(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v}
    keys = sorted(kwargs.keys())
    return '&'.join(['%s=%s' % (key, kwargs[key]) for key in keys])


def add_key(string_to_sign, key):
    return '{0}&key={1}'.format(string_to_sign, key)


def calc_md5(string_to_hash):
    return hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()


def huan_ji_xia_encryption(json_payload):
    sec_key = 'm2cjgx46md5973n4ymeoxa4v195iwwmb'
    to_sign = {}
    for element in json_payload:
        to_sign.update(json_payload[element])
    to_sign = key_value_sort_join(**to_sign)
    to_sign = '{0}&key={1}'.format(to_sign, sec_key)
    sign = calc_md5(to_sign)
    if 'params' in json_payload:
        json_payload['params']['sign'] = sign
    elif '__param' in json_payload:
        json_payload['_param']['sign'] = sign
    return json_payload
