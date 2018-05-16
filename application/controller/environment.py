# -*- coding: utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import environment as EnvironmentAPI
from application.api import use_case as UseCaseAPI


@app.route('/environment/line/add', methods=['POST'])
def add_environment_line():
    """
    添加environment_line
    """
    try:
        environment_line_id = EnvironmentAPI.add_environment_line(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': environment_line_id})


@app.route('/environment/line_info/add', methods=['POST'])
def add_environment_line_info():
    """
    添加environment_line_info
    """
    try:
        environment_info_id = EnvironmentAPI.add_environment_line_info(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': environment_info_id})


@app.route('/environment/line/modify', methods=['POST'])
def update_environment_line():
    """
    更新environment_line
    """
    try:
        environment_line_id = EnvironmentAPI.modify_environment_line(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': environment_line_id})


@app.route('/environment/line_info/modify', methods=['POST'])
def update_environment_line_info():
    """
    更新environment_line_info
    """
    try:
        environment_info_id = EnvironmentAPI.modify_environment_line_info(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': environment_info_id})


@app.route('/environment/line/delete', methods=['POST'])
def del_environment_line():
    """
    删除environment_line
    """
    try:
        environment_line_id = EnvironmentAPI.del_environment_line(**request.get_json())
        use_case_info_list = UseCaseAPI.get_use_case(environment_id=request.get_json().get('id'))
        for use_case_info in use_case_info_list:
            UseCaseAPI.modify_use_case(id=use_case_info.get('id'), environment_id=0)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': environment_line_id})


@app.route('/environment/line_info/delete', methods=['POST'])
def del_environment_line_info():
    """
    删除environment_line_info
    """
    try:
        environment_info_id = EnvironmentAPI.del_environment_line_info(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': environment_info_id})


@app.route('/environment/line/detail', methods=['POST'])
def get_environment_line():
    """
    查询environment_line
    :return:返回一个environment_line列表
    """

    try:
        environment_line_list = EnvironmentAPI.get_environment_line(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': environment_line_list})


@app.route('/environment/line_info/detail', methods=['POST'])
def get_environment_line_info():
    """
    查询environment_line_info
    :return:返回一个environment_line_info列表
    """
    try:
        environment_info_list = EnvironmentAPI.get_environment_line_info(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': environment_info_list})
