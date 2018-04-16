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
        # TODO 接入权限系统后移除写死创建人
        parameter_json = request.get_json()
        parameter_json['create_by'] = 1
        parameter_id = ParameterAPI.add_parameter(**parameter_json)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': parameter_id})


@app.route('/parameter/info', methods=['POST'])
def parameter_info():
    """
    获取parameter列表
    :param
        pageIndex, 需要第几页
        pageSize, 页面显示个数
    :return
    """
    param_json = request.get_json()
    pageIndex = int(param_json.pop('pageIndex')) if 'pageIndex' in param_json else 1
    pageSize = int(param_json.pop('pageSize')) if 'pageSize' in param_json else 10
    try:
        result = ParameterAPI.get_parameter(**param_json)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result[int(pageIndex-1)*int(pageSize):int(pageIndex)*int(pageSize)]})


@app.route('/parameter/count', methods=['GET'])
def parameter_count():
    """
    获取parameter总个数
    """
    try:
        result = ParameterAPI.query_parameter_count()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/parameter/update', methods=['POST'])
def update_parameter():
    """
    修改parameter
    """
    try:
        parameter_id = ParameterAPI.modify_parameter(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': parameter_id})


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
