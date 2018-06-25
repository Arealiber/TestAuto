# -*- coding:utf-8 -*-
from flask import request, jsonify
from application import app
from application.controller import login_required, localhost_required
from application.util.exception import try_except
from application.api import email as EmailAPI
from application.util.email_send import email_send


@app.route('/email/send', methods=['POST'])
@try_except
@localhost_required
def email_send():
    """
    发送email到指定邮箱
    :return:
    """
    result = EmailAPI.query_email_account(**request.get_json())
    email_data = {}
    for emai_account in result:
        email_data[emai_account.get('email_name')] = emai_account.get('email_address')

    return jsonify({'success': True})


@app.route('/email/account/add', methods=['POST'])
@try_except
@login_required
def email_account_add():
    """
    添加要发送的邮箱地址
    :return:
    """
    EmailAPI.add_email_account(**request.get_json())
    return jsonify({'success': True})


@app.route('/email/account/delete', methods=['POST'])
@try_except
@login_required
def email_account_delete():
    """
    删除指定的邮箱地址
    :return:
    """
    EmailAPI.del_email_account(**request.get_json())
    return jsonify({'success': True})


@app.route('/email/account/info', methods=['POST'])
@try_except
@login_required
def email_account_info():
    """
    查询邮箱地址
    :return:
    """
    result = EmailAPI.query_email_account(**request.get_json())
    return jsonify({'success': True, 'res': result})
