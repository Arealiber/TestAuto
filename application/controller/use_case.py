# -*- coding:utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import interface as InterfaceAPI
from application.api import use_case as Case_API
from application.util.parameter import *
from application.util import execute_test as Exec

"""
用例

"""


@app.route('/use_case/add', methods=['POST'])
def add_use_case():
    """
    功能描述: 添加use_case，只包含用例基础信息
    :return:
    """
    try:
        # TODO 接入权限系统后移除写死创建人
        use_case_json = request.get_json()
        use_case_json['create_by'] = 1
        use_case_id = Case_API.add_use_case(**use_case_json)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': use_case_id})


@app.route('/use_case/list', methods=['POST'])
def use_case_list():
    """
    获取use_case列表，不需要获取与use_case关联的interface
    :return:
    """
    param_json = request.get_json()
    page_index = int(param_json.pop('pageIndex')) if 'pageIndex' in param_json else 1
    page_size = int(param_json.pop('pageSize')) if 'pageSize' in param_json else 10
    try:
        result = Case_API.get_use_case(**param_json)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    if not(page_index and page_size):
        return jsonify({'success': True, 'res': result})
    return jsonify({'success': True, 'res': result[(page_index - 1) * page_size:page_index * page_size]})


@app.route('/use_case/count', methods=['GET'])
def use_case_count():
    """
    获取use_case的总个数
    :return:
    """
    try:
        result = Case_API.query_use_case_count()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/use_case/detail', methods=['POST'])
def use_case_detail():
    """
    功能描述: 获取某个use_case的详细信息，包括其包含的interface列表
    1. 根据use_case_id获取use_case基本信息
    2. 根据use_case_id获取use_case与interface的关联信息
    3. 根据关联信息的id查出所有interface的名称信息以及定义的参数信息
    4. 信息整理并返回
    :return:
    """
    try:
        use_case_info = Case_API.get_use_case(**request.get_json())[0]
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    use_case_info.update({'interface_list': []})
    try:
        relation_interface_list = Case_API.get_relation(use_case_id=use_case_info.get('id'))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    for relation_interface in relation_interface_list:
        relation_interface.pop('use_case_id')
        relation_interface.pop('create_time')
        relation_interface.pop('update_time')
        interface_id = relation_interface.get('interface_id')
        interface_list = InterfaceAPI.get_interface(id=interface_id)
        relation_interface.update({'interface_name': interface_list[0].get('interface_name')})
        para_list = Case_API.get_case_parameter_relation(relation_id=relation_interface['id'])
        relation_interface.update({'param_list': para_list})
        use_case_info['interface_list'].append(relation_interface)
    return jsonify({'success': True, 'res': use_case_info})


@app.route('/use_case/update', methods=['POST'])
def update_use_case():
    """
    功能描述: 更新use_case内容，不更新与interface的关联
    :return:
    """
    try:
        use_case_id = Case_API.modify_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res' : use_case_id})


@app.route('/use_case/delete', methods=['POST'])
def del_use_case():
    """
    功能描述: 删除use_case
    :return:
    """
    try:
        Case_API.del_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/use_case/execute', methods=['POST'])
def execute_use_case():
    """
    手动执行某个use_case
    先不写，等测试流程实现再补上
    :return:
    """
    use_case_id = request.get_json()['id']
    result = Exec.run_use_case(use_case_id)
    return jsonify({'success': True, 'res': result})


@app.route('/use_case/relation/add', methods=['POST'])
def add_relation():
    """
    功能描述: 将某个interface与某个use_case关联
    1. 关联use_case与interface
    2. 查找interface内parameter信息, 用空值为每个参数在relation下生成记录
    :return:
    """
    interface_id = request.get_json().get('interface_id')
    try:
        relation_id = Case_API.add_relation(**request.get_json())
        interface_list = InterfaceAPI.get_interface(id=interface_id)
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    the_interface = interface_list[0]
    analysis_str = ''.join([the_interface.get('interface_header'),
                            the_interface.get('interface_json_payload'),
                            the_interface.get('interface_url')])
    param_list = search_parameter(analysis_str)
    for para in param_list:
        Case_API.add_case_parameter_relation(relation_id=relation_id, parameter_name=para, parameter_value='')
    return jsonify({'success': True})


@app.route('/use_case/relation/update_eval', methods=['POST'])
def update_eval():
    """
    更新eval_string的值
    :return:
    """
    try:
        Case_API.update_eval_relation(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True})


@app.route('/use_case/relation/delete', methods=['POST'])
def del_relation():
    """
    功能描述: 解除某个interface与use_case的关联
    :return:
    """
    try:
        id_to_delete = request.get_json()['id']
        Case_API.del_relation(id_to_delete)
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True})


@app.route('/use_case/relation/reorder', methods=['POST'])
def reorder_relation():
    """
    功能描述: 重新排序某个interface在use_case中的顺序
    :return:
    """
    try:
        relation_id = request.get_json()['id']
        new_order = request.get_json()['new_order']
        Case_API.reorder_relation(relation_id, new_order)
    except Exception as e:
        return jsonify({'success':False, 'res':str(e)})
    return jsonify({'success': True})


@app.route('/use_case/relation/parameter/modify', methods=['POST'])
def relation_update_parameter():
    """
    功能描述: 更新某个use_case传给interface的参数的信息
    :return:
    """
    try:
        Case_API.modify_case_parameter_relation(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})
