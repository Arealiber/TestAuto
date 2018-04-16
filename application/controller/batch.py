# -*- coding:utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import batch as BatchAPI
from application.schema import schema


@app.route('/batch/add', methods=['POST'])
def add_batch():
    """
    create batch for use case
    :return:
    """
    try:
        schema.add_batch_schema(request.get_json())
        BatchAPI.add_batch(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/batch/info', methods=['POST'])
def get_batch():
    """
    query batch of use case
    :return:
    """
    param_json = request.get_json()
    pageIndex = int(param_json.pop('pageIndex')) if 'pageIndex' in param_json else 1
    pageSize = int(param_json.pop('pageSize')) if 'pageSize' in param_json else 10
    try:
        result = BatchAPI.get_batch(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result[(pageIndex-1)*pageSize:pageIndex*pageSize]})


@app.route('/batch/count', methods=['GET'])
def query_batch_count():
    """
    query batch count of use case
    :return:
    """
    try:
        result = BatchAPI.query_batch_count()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/batch/update', methods=['POST'])
def modify_batch():
    """
    create batch for use case
    :return:
    """
    try:
        BatchAPI.modify_batch(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/batch/delete', methods=['POST'])
def delete_batch():
    """
    删除用例批次，并解除批次关联的用例
    :return:
    """
    try:
        BatchAPI.del_batch(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/batch/relation/add', methods=['POST'])
def add_batch_use_case_relation():
    """
    往某一个批次添加用例
    :return:
    """
    try:
        BatchAPI.add_batch_use_case_relation(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/batch/relation/info', methods=['POST'])
def get_batch_use_case_relation():
    """
    查询某一个批次已添加的用例列表
    :return:{'success': True, 'res': relation_use_case_list}
    """
    try:
        result = BatchAPI.get_batch_use_case_relation(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/batch/relation/delete', methods=['POST'])
def del_batch_use_case_relation():
    """
    查询某一个批次已添加的用例列表
    :return:{'success': True, 'res': relation_use_case_list}
    """
    try:
        BatchAPI.del_batch_use_case_relation(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})

