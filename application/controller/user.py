# -*- coding:utf-8 -*-

from flask import request, jsonify

from application import app
from application.api import user as UserAPI


@app.route('/user/add', methods=['POST'])
def add_user():
    try:
        result = UserAPI.add_user(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/user/info', methods=['POST'])
def user_info():
    result = UserAPI.get_user(**request.get_json())
    user_list = []
    for user in result:
        user_list.append(user.to_dict())
    return jsonify({'success': True, 'res': user_list})


@app.route('/user/update', methods=['POST'])
def update_user():
    try:
        result = UserAPI.modify_user(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/user/delete', methods=['POST'])
def delete_user():
    try:
        result = UserAPI.del_user(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True, 'res': result})
