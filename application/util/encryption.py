import hashlib


def key_value_sort_join(**kwargs):
    """
    根据传入的key value pair按ASCII升序排序并用&链接
    :param kwargs:      key value pair
    :return:            排序并链接过后的字符串
    """
    kwargs = {k: v for k, v in kwargs.items() if v}
    keys = sorted(kwargs.keys())
    return '&'.join(['%s=%s' % (key, kwargs[key]) for key in keys])


def add_key(string_to_sign, key):
    """
    将key用&key=加入到给定字符串的最后
    :param string_to_sign:  给定字符串
    :param key:             key
    :return:                添加了key的字符串
    """
    return '{0}&key={1}'.format(string_to_sign, key)


def calc_md5(string_to_hash):
    """
    计算传入内容的md5
    :param string_to_hash:  传入内容
    :return:                传入内容的md5
    """
    return hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()


def huan_ji_xia_encryption(json_payload):
    """
    换机侠的加密方式
    :param json_payload:    需要加密的json
    :return:                添加了签名的json
    """
    sec_key = 'm2cjgx46md5973n4ymeoxa4v195iwwmb'
    to_sign = {}
    for element in json_payload:
        to_sign.update(json_payload[element])
    to_sign = key_value_sort_join(**to_sign)
    to_sign = '{0}&key={1}'.format(to_sign, sec_key)
    sign = calc_md5(to_sign)
    if 'params' in json_payload:
        json_payload['params']['sign'] = sign
    elif '_param' in json_payload:
        json_payload['_param']['sign'] = sign
    return json_payload
