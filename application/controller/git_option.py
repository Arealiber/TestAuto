# -*- coding:utf-8 -*-
from flask import request, jsonify
from application import app
from application.util.exception import try_except
from application.controller import login_required
from application.util import git_option as gitAPI


@app.route('/git/create_tag', methods=['POST'])
@try_except
@login_required
def create_tag():
    """
    功能描述: 创建一个tag
    :return:
    """
    soft_name = request.get_json()['soft_name']
    work_path = request.get_json()['work_path']
    if not (soft_name or work_path):
        return jsonify({'success': False, 'res': '参数错误'})
    tag = gitAPI.create_tag(soft_name, work_path)
    if not tag:
        return jsonify({'success': False, 'res': '创建tag失败'})
    return jsonify({'success': True, 'res': tag})



