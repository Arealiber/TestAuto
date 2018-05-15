from flask import jsonify

from application import app
from application.api import encryption as EncryptionAPI
from application.util.exception import try_except


@app.route('/encryption/list')
@try_except
def encryption_list():
    return jsonify(EncryptionAPI.get_encryption_list())
