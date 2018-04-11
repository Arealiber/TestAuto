# -*- coding:utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import interface as InterfaceAPI
from application.api import use_case as Case_API
from application.schema import schema


"""
用例

"""


@app.route('/use_case/add', methods=['POST'])
def add_use_case():
    """
    添加use_case，只包含用例基础信息
    """
    try:
        Case_API.add_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/use_case/list', methods=['POST'])
def use_case_list():
    """
    获取use_case列表，不需要获取与use_case关联的interface
    """
    try:
        result = Case_API.get_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    use_case_list = []
    for case_info in result:
        use_case_list.append(case_info.to_dict())
    return jsonify(use_case_list)


@app.route('/use_case/detail', methods=['POST'])
def use_case_detail():
    """
    获取某个use_case的详细信息，包括其包含的interface列表
    1. 根据use_case_id获取use_case基本信息
    2. 根据use_case_id获取use_case与interface的关联信息
    3. 根据关联信息的id查出所有interface的名称信息以及定义的参数信息
    4. 信息整理并返回
    """
    try:
        schema.use_case_schema(request.get_json())
        result = Case_API.get_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    use_case_list = []
    for use_case in result:
        use_case_list.append(use_case.to_dict())
    use_case_info = use_case_list[0]
    use_case_info.update({'interface_list':[]})
    try:
        relation_interface_list = Case_API.get_relation(use_case_info.get('id'))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    for relation_interface in relation_interface_list:
        relation_interface.pop('use_case_id')
        interface_id = relation_interface.pop('interface_id')
        use_case_info['interface_list'].append(relation_interface)

    return jsonify({'success': True, 'res':use_case_info})


@app.route('/use_case/update', methods=['POST'])
def update_use_case():
    """
    更新use_case内容，不更新与interface的关联
    """
    try:
        Case_API.modify_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/use_case/delete', methods=['POST'])
def del_use_case():
    """
    删除use_case
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
    """
    pass


@app.route('/use_case/relation/add', methods=['POST'])
def add_relation():
    """
    将某个interface与某个use_case关联
    1. 关联use_case与interface
    2. 查找interface内parameter信息, 用空值为每个参数在relation下生成记录
    """
    pass


@app.route('/use_case/relation/delete', methods=['POST'])
def del_relation():
    """
    解除某个interface与use_case的关联
    """
    pass


@app.route('/use_case/relation/reorder', methods=['POST'])
def reorder_relation():
    """
    重新排序某个interface在use_case中的顺序
    """
    pass


@app.route('/use_case/relation/parameter/modify', methods=['POST'])
def relation_update_parameter():
    """
    更新某个
    """
    pass
