from flask import jsonify
from functools import wraps
from application import app

if not app.config['DEBUG']:
    from application.util import logger as LOGGER


def try_except(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            error_str = '{0}: {1}'.format(str(e.__class__.__name__), str(e))
            if not app.config['DEBUG']:
                LOGGER.exception_log(error_str)
            return jsonify({'success': False, 'error': str(e)})
    return wrapped
