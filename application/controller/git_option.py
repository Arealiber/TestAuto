# -*- coding:utf-8 -*-
from flask import request, jsonify
from application import app
from application.util.exception import try_except
from application.controller import login_required
from application.api import git_option as gitAPI


@app.route('/git/create_tag', methods=['POST'])
@try_except
@login_required
def create_tag():
    """
    功能描述: 创建一个tag
    :return:
    """
    tag = request.get_json()['tag']
    result = gitAPI.create_tag(tag)
    return jsonify({'success': True, 'res': result})




