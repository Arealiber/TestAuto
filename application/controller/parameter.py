# -*- coding: utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import parameter as ParameterAPI


@app.route('/parameter/add', methods=['POST'])
def add_parameter():
    """
    添加parameter
    """
    try:
        ParameterAPI.add_parameter(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/parameter/info', methods=['POST'])
def parameter_info():
    """
    获取parameter列表
    """
    try:
        result = ParameterAPI.get_parameter(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/parameter/update', methods=['POST'])
def update_parameter():
    """
    修改parameter
    """
    try:
        ParameterAPI.modify_parameter(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/parameter/delete', methods=['POST'])
def delete_parameter():
    """
    删除parameter
    """
    try:
        ParameterAPI.del_parameter(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})
