from flask import request, jsonify
from application import app
from application.api import parameter as ParameterAPI


@app.route('/parameter/add', methods=['POST'])
def add_parameter():
    try:
        ParameterAPI.add_parameter(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/parameter/info', methods=['POST'])
def parameter_info():
    try:
        result = ParameterAPI.get_parameter(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    parameter_list = []
    for parameter in result:
        parameter_list.append(parameter.to_dict())
    return jsonify(parameter_list)


@app.route('/parameter/update', methods=['POST'])
def update_parameter():
    try:
        ParameterAPI.modify_parameter(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})


@app.route('/parameter/delete', methods=['POST'])
def delete_parameter():
    try:
        ParameterAPI.del_parameter(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': True})
