# -*- coding:utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import batch as BatchAPI
from application.api import use_case as UseCaseAPI
from application.util import execute_test as Exec
from application.util.exception import try_except


@app.route('/batch/add', methods=['POST'])
@try_except
def add_batch():
    """
    create batch for use case
    :return:
    """
    # TODO 接入权限系统后移除写死创建人
    # schema.add_batch_schema(request.get_json())
    batch_json = request.get_json()
    batch_json['create_by'] = 1
    batch_id = BatchAPI.add_batch(**batch_json)
    return jsonify({'success': True, 'res': batch_id})


@app.route('/batch/info', methods=['POST'])
@try_except
def get_batch():
    """
    query batch of use case
    :return:
    """
    param_json = request.get_json()
    page_index = int(param_json.pop('pageIndex')) if 'pageIndex' in param_json else 1
    page_size = int(param_json.pop('pageSize')) if 'pageSize' in param_json else 10
    result = BatchAPI.get_batch(**param_json)
    return jsonify({'success': True, 'res': result[(page_index - 1) * page_size:page_index * page_size]})


@app.route('/batch/detail', methods=['POST'])
@try_except
def batch_detail():
    """

    :return:
    """
    batch = BatchAPI.get_batch(**request.get_json())[0]
    relation_list = BatchAPI.get_batch_use_case_relation(batch_id=batch['id'])
    batch['use_case_list'] = []
    for relation in relation_list:
        use_case = UseCaseAPI.get_use_case(id=relation['use_case_id'])[0]
        batch['use_case_list'].append({
            'id': relation['id'],
            'use_case_name': use_case['use_case_name'],
            'desc': use_case['desc']
        })
    return jsonify({'success': True, 'res': batch})


@app.route('/batch/count', methods=['GET'])
@try_except
def query_batch_count():
    """
    query batch count of use case
    :return:
    """
    result = BatchAPI.query_batch_count()
    return jsonify({'success': True, 'res': result})


@app.route('/batch/update', methods=['POST'])
@try_except
def modify_batch():
    """
    create batch for use case
    :return:
    """
    batch_id = BatchAPI.modify_batch(**request.get_json())
    return jsonify({'success': True, 'res': batch_id})


@app.route('/batch/delete', methods=['POST'])
@try_except
def delete_batch():
    """
    删除用例批次，并解除批次关联的用例
    :return:
    """
    BatchAPI.del_batch(**request.get_json())
    return jsonify({'success': True})


@app.route('/batch/relation/add', methods=['POST'])
@try_except
def add_batch_use_case_relation():
    """
    往某一个批次添加用例
    :return:
    """
    batch_id = request.get_json()['batch_id']
    use_case_id = request.get_json()['use_case_id']
    BatchAPI.add_batch_use_case_relation(batch_id, use_case_id)
    return jsonify({'success': True})


@app.route('/batch/relation/info', methods=['POST'])
@try_except
def get_batch_use_case_relation():
    """
    查询某一个批次已添加的用例列表
    :return:{'success': True, 'res': relation_use_case_list}    """
    result = BatchAPI.get_batch_use_case_relation(**request.get_json())
    relation_use_case_id_list = [(res.get('use_case_id'), res.get('id')) for res in result]
    use_case_info_lst = []
    for relation_id_use_case_id_tuple in relation_use_case_id_list:
        use_case_info = UseCaseAPI.get_use_case(id=relation_id_use_case_id_tuple[0])[0]
        use_case_info.update({'id': relation_id_use_case_id_tuple[1]})
        use_case_info_lst.append(use_case_info)
    batch_use_case_relation_info = result[-1]
    batch_use_case_relation_info.pop('use_case_id')
    batch_use_case_relation_info.pop('id')
    batch_use_case_relation_info.update({'use_case_info': use_case_info_lst})
    return jsonify({'success': True, 'res': batch_use_case_relation_info})


@app.route('/batch/relation/delete', methods=['POST'])
@try_except
def del_batch_use_case_relation():
    """
    删除某一个批次已添加的用例列表
    :return:{'success': True, 'res': relation_use_case_list}
    """
    relation_id = request.get_json()['id']
    BatchAPI.del_batch_use_case_relation(relation_id)
    return jsonify({'success': True})


@app.route('/batch/execute', methods=['POST'])
@try_except
def batch_execute():
    batch_id = request.get_json()['id']
    Exec.run_batch(batch_id)
    return jsonify({'success': True})


@app.route('/batch/auto_run')
@try_except
def batch_auto_run():
    batch_list = BatchAPI.get_batch(auto_run=True)
    for batch in batch_list:
        Exec.run_batch(batch['id'], True)
    return jsonify({'success': True})
