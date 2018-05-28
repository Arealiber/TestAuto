from importlib import import_module

from application import app
from application.util.import_util import import_sub_module
from flask_cache import Cache

ctrl_pkg_module = import_module('application.controller')
import_sub_module(ctrl_pkg_module)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
