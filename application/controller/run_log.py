# -*- coding:utf-8 -*-
from flask import request, jsonify
from application.api import run_log as RunLogAPI
from application.api import use_case as UseCaseAPI
from application.api import interface as InterfaceAPI
from application import app


@app.route('/run_log/batch/add', methods=['POST'])
def add_batch_run_log():
    """
    :return:
    """
    try:
        result = RunLogAPI.add_batch_run_log(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True, 'res': str(result)})


@app.route('/run_log/batch/info', methods=['POST'])
def get_multi_batch_run_log_info():
    """
    :return:
    """
    print(request.get_json())
    try:
        result = RunLogAPI.get_multi_batch_run_log_info(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/run_log/use_case/add', methods=['POST'])
def add_use_case_run_log():
    """
    :return:
    """
    print(request.get_json())
    try:
        RunLogAPI.add_use_case_run_log(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True})


@app.route('/run_log/use_case/info', methods=['POST'])
def get_use_case_run_log():
    """
    :return:
    """
    try:
        result = RunLogAPI.get_use_case_run_log(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    for use_case_run_log_dict in result:
        use_case_id = use_case_run_log_dict.get('use_case_id')
        try:
            use_case_info = UseCaseAPI.get_single_use_case(use_case_id)
        except Exception as e:
            return jsonify({'success': False, 'res': str(e)})
        use_case_name = use_case_info.get('use_case_name')
        use_case_run_log_dict.update({'use_case_name': use_case_name})
    return jsonify({'success': True, 'res': result})


@app.route('/run_log/use_case/add', methods=['POST'])
def add_interface_run_log():
    """
    :return:
    """
    print(request.get_json())
    try:
        RunLogAPI.add_interface_run_log(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True})


@app.route('/run_log/interface/info', methods=['POST'])
def get_interface_run_log():
    """
    :param: 必须需要传入use_case_run_log_id
    :return:
    """
    try:
        result = RunLogAPI.get_interface_run_log(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    for interface_run_log_dict in result:
        interface_id = interface_run_log_dict.get('interface_id')
        try:
            interface_info = InterfaceAPI.query_single_interface(interface_id)
        except Exception as e:
            return jsonify({'success': False, 'res': str(e)})
        interface_name = interface_info.get('interface_name')
        interface_run_log_dict.update({'interface_name': interface_name})
    return jsonify({'success': True, 'res': result})
