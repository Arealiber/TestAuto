# -*- coding: utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import interface as InterfaceAPI


@app.route('/interface/add', methods=['POST'])
def add_interface():
    try:
        InterfaceAPI.add_interface(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/interface/info', methods=['POST'])
def get_interface():
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
    try:
        InterfaceAPI.modify_interface(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/interface/delete', methods=['POST'])
def delete_interface():
    try:
        InterfaceAPI.del_interface(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})
