# -*- coding:utf-8 -*-

from flask import request, jsonify

from application import app
from application.api import user as UserAPI
from application.schema.schema import *
from application.util.exception import try_except


@app.route('/user/add', methods=['POST'])
@try_except
def add_user():
    user_schema(request.json)
    result = UserAPI.add_user(**request.get_json())
    return jsonify({'success': True, 'res': result})


@app.route('/user/info', methods=['POST'])
@try_except
def user_info():
    result = UserAPI.get_user(**request.get_json())
    user_list = []
    for user in result:
        user_list.append(user.to_dict())
    return jsonify({'success': True, 'res': user_list})


@app.route('/user/update', methods=['POST'])
@try_except
def update_user():
    result = UserAPI.modify_user(**request.get_json())
    return jsonify({'success': True, 'res': result})


@app.route('/user/delete', methods=['POST'])
@try_except
def delete_user():
    result = UserAPI.del_user(**request.get_json())
    return jsonify({'success': True, 'res': result})
