# -*- coding: utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import environment as EnvironmentAPI
from application.util.exception import try_except


@app.route('/environment/line/add', methods=['POST'])
@try_except
def add_environment_line():
    """
    添加environment_line
    """
    environment_line_id = EnvironmentAPI.add_environment_line(**request.get_json())
    return jsonify({'success': True, 'res': environment_line_id})


@app.route('/environment/line_info/add', methods=['POST'])
@try_except
def add_environment_line_info():
    """
    添加environment_line_info
    """
    environment_info_id = EnvironmentAPI.add_environment_line_info(**request.get_json())
    return jsonify({'success': True, 'res': environment_info_id})


@app.route('/environment/line/modify', methods=['POST'])
@try_except
def update_environment_line():
    """
    更新environment_line
    """
    environment_line_id = EnvironmentAPI.modify_environment_line(**request.get_json())
    return jsonify({'success': True, 'res': environment_line_id})


@app.route('/environment/line_info/modify', methods=['POST'])
@try_except
def update_environment_line_info():
    """
    更新environment_line_info
    """
    environment_info_id = EnvironmentAPI.modify_environment_line_info(**request.get_json())
    return jsonify({'success': True, 'res': environment_info_id})


@app.route('/environment/line/delete', methods=['POST'])
@try_except
def del_environment_line():
    """
    删除environment_line
    """
    environment_line_id = EnvironmentAPI.del_environment_line(**request.get_json())
    return jsonify({'success': True, 'res': environment_line_id})


@app.route('/environment/line_info/delete', methods=['POST'])
@try_except
def del_environment_line_info():
    """
    删除environment_line_info
    """
    environment_info_id = EnvironmentAPI.del_environment_line_info(**request.get_json())
    return jsonify({'success': True, 'res': environment_info_id})


@app.route('/environment/line/delete', methods=['POST'])
@try_except
def get_environment_line():
    """
    查询environment_line
    :return:返回一个environment_line列表
    """
    environment_line_list = EnvironmentAPI.get_environment_line(**request.get_json())
    return jsonify({'success': True, 'res': environment_line_list})


@app.route('/environment/line_info/delete', methods=['POST'])
@try_except
def get_environment_line_info():
    """
    查询environment_line_info
    :return:返回一个environment_line_info列表
    """
    environment_info_list = EnvironmentAPI.get_environment_line_info(**request.get_json())
    return jsonify({'success': True, 'res': environment_info_list})



