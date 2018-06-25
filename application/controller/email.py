# -*- coding:utf-8 -*-
from flask import request, jsonify
from application import app
from application.controller import login_required
from application.util.exception import try_except


@app.route('/email/send', methods=['POST'])
@try_except
@login_required
def email_send():
    """
    发送email到指定邮箱
    :return:
    """

    return jsonify({'success': True})
