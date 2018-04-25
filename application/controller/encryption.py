from flask import jsonify

from application import app
from application.api import encryption as EncryptionAPI


@app.route('/get/encryption')
def get_encryption():
    return jsonify(EncryptionAPI.get_encryption_list())
