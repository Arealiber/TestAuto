# -*- coding:utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import use_case as UseCaseAPI


@app.route('/case/add', methods=['POST'])
def add_use_case():
    try:
        result = UseCaseAPI.add_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    return jsonify({'success': True, 'res': result})


@app.route('/case/info', methods=['POST'])
def get_use_case():
    try:
        result = UseCaseAPI.get_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    case_list = []
    for use_case in result:
        case_list.append(use_case.to_dict())
    return jsonify({'success': False, 'res': case_list})


@app.route('/case/update', methods=['POST'])
def modify_use_case():
    try:
        result = UseCaseAPI.modify_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/case/delete', methods=['POST'])
def del_use_case():
    try:
        result = UseCaseAPI.del_use_case(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})
