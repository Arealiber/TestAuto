from flask import jsonify
from functools import wraps


def try_except(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    return wrapped
