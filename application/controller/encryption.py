from flask import jsonify

from application import app
from application.api import encryption as EncryptionAPI


@app.route('/encryption/list')
def encryption_list():
    return jsonify(EncryptionAPI.get_encryption_list())
