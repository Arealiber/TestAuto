# -*- coding: utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import interface as InterfaceAPI
from application.api import use_case as UseCaseAPI
from application.util.parameter import search_parameter


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
    return jsonify({'success': True, 'res': results})


@app.route('/interface/update', methods=['POST'])
def modify_interface():
    """
    更新interface信息
    1. 获取原interface参数信息
    2. 将更新的interface内容写入数据库
    3. 如果新旧参数无区别, 结束并返回
    4. 如果新旧参数有区别, 更新所有use_case传给此interface的参数记录
    """
    interface_id = request.get_json().get('id')
    try:
        interface_old_info = InterfaceAPI.get_interface(id=interface_id)[0]
        InterfaceAPI.modify_interface(**request.get_json())
        interface_new_info = InterfaceAPI.get_interface(id=interface_id)[0]
        relation_list = UseCaseAPI.get_relation(interface_id=interface_id)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    old_analysis_str = ''.join([interface_old_info.get('interface_header'),
                                interface_old_info.get('interface_json_payload'),
                                interface_old_info.get('interface_url')])
    new_analysis_str = ''.join([interface_new_info.get('interface_header'),
                                interface_new_info.get('interface_json_payload'),
                                interface_new_info.get('interface_url')])
    old_param_list = search_parameter(old_analysis_str)
    new_param_list = search_parameter(new_analysis_str)
    update_param_list = list(set(old_param_list) ^ set(new_param_list))
    if len(update_param_list) == 0:
        return jsonify({'success': True})
    else:
        for param in update_param_list:
            if param in old_param_list:
                for p_relation in relation_list:
                    try:
                        UseCaseAPI.del_case_parameter_relation(parameter_name=param, relation_id=p_relation['id'])
                    except Exception as e:
                        return jsonify({'success': False, 'err': 'del case relative param fail{0}'.format(str(e))})
            else:  # 新增参数添加到各个用例中去
                for relation in relation_list:
                    kwargs = {'relation_id': relation['id'],
                              'parameter_name': param,
                              'parameter_value': ''}
                    try:
                        UseCaseAPI.add_case_parameter_relation(**kwargs)
                    except Exception as e:
                        return jsonify({'success': False, 'err': 'add case para relation failure %s'% str(e)})
    return jsonify({'success': True})


@app.route('/interface/delete', methods=['POST'])
def delete_interface():
    """
    删除某个interface
    1. 将interface数据从数据库中标记为已删除
    2. 将所有use_case与此interface的关联关系标记为已删除
    3. 将所有use_case传给此interface的参数记录标记为已删除
    """
    interface_id = request.get_json().get('id')
    try:
        relation_list = UseCaseAPI.get_relation(interface_id=interface_id)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    for interface_relation in relation_list:
        try:
            parameter_info = UseCaseAPI.get_case_parameter_relation(id=interface_relation['id'])
            for s_prama_relation in parameter_info:
                UseCaseAPI.del_case_parameter_relation(id=s_prama_relation['id'])
            UseCaseAPI.del_relation(interface_relation['id'])
        except Exception as e:
            return jsonify({'success': False, 'err': str(e)})
    InterfaceAPI.del_interface(**request.get_json())
    return jsonify({'success': True})
