from flask import jsonify


def try_except(fn):
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    return wrapped
