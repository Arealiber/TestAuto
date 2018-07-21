# -*- coding:utf-8 -*-
from flask import request, jsonify, session
from application import app
from application.controller import login_required, localhost_required
from application.util.exception import try_except
from application.api import email as EmailAPI
from application.util import email_send as EmailSendAPI


@app.route('/email/send', methods=['GET'])
@try_except
@localhost_required
def email_send():
    """
    发送email到指定邮箱
    :return:
    #TODO: 发送邮件时发件人设置，等邮件系统改好后添加
    """
    email_data = dict()
    email_data['address'] = dict()
    email_data['str_url'] = 'http://push.huanjixia.com/email-interface'
    email_data['title'] = '自动化巡检报表'
    if app.config['PROXIES']:
        email_data['proxies'] = {'http': app.config['DB_URI'].split('@')[1].split('/')[0]}  # 取开发机ip作为代理服务器

    result = EmailAPI.query_email_account()
    if not result:
        return jsonify({'success': False, 'res': '邮箱不能为空'})
    for emai_account in result:
        email_data['address'][emai_account.get('email_name')] = emai_account.get('email_address')

    data_body = EmailSendAPI.get_send_body()
    if not data_body:
        data_body = '获取日志报表数据失败'
    email_data['body'] = str(data_body)
    ret = EmailSendAPI.email_send(**email_data)
    if ret == 0:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'res': '发送失败:{}'.format(ret)})


@app.route('/email/account/add', methods=['POST'])
@try_except
@login_required
def email_account_add():
    """
    添加要发送的邮箱地址
    :return:
    """
    kwarg = request.get_json()
    if not (kwarg.get('email_name') and kwarg.get('email_address')):
        return jsonify({'success': False, 'error': '用户名或地址不能为空'})
    elif '@' not in kwarg.get('email_address'):
        return jsonify({'success': False, 'error': '邮箱格式错误请正确填写（template@huishoubao.com.cn）'})
    else:
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
    real_name = session['real_name']
    if real_name not in ['李成波', '汪林云', '赵军', '刘渊', '管理员']:
        return jsonify({'success': False, 'error': '无该功能权限，请找相关开发人员给配置权限'})
    result = EmailAPI.query_email_account()
    return jsonify({'success': True, 'res': result})
