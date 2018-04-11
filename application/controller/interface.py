# -*- coding: utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import interface as InterfaceAPI
from application.api import use_case as UseCaseAPI


@app.route('/interface/add', methods=['POST'])
def add_interface():
    """
    添加interface
    """
    try:
        InterfaceAPI.add_interface(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/interface/info', methods=['POST'])
def get_interface():
    """
    根据过滤规则获取interface列表, 无规则则返回所有interface
    """
    try:
        results = InterfaceAPI.get_interface(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    interface_list = []
    for interface in results:
        interface_list.append(interface.to_dict())
    return jsonify(interface_list)


@app.route('/interface/update', methods=['POST'])
def modify_interface():
    """
    更新interface信息
    1. 获取原interface参数信息
    2. 将更新的interface内容写入数据库
    3. 如果新旧参数无区别, 结束并返回
    4. 如果新旧参数有区别, 更新所有use_case传给此interface的参数记录
    """
    try:
        InterfaceAPI.modify_interface(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/interface/delete', methods=['POST'])
def delete_interface():
    """
    删除某个interface
    1. 将interface数据从数据库中标记为已删除
    2. 将所有use_case与此interface的关联关系标记为已删除
    3. 将所有use_case传给此interface的参数记录标记为已删除
    """
    try:
        InterfaceAPI.del_interface(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})
