import hashlib


def key_value_sort_join(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v}
    keys = sorted(kwargs.keys())
    return '&'.join(['%s=%s' % (key, kwargs[key]) for key in keys])


def add_key(string_to_sign, key):
    return '{0}&key={1}'.format(string_to_sign, key)


def calc_md5(string_to_hash):
    return hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()
