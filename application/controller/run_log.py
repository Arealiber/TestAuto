# -*- coding:utf-8 -*-
from flask import request, jsonify
from application.api import run_log as RunLogAPI
from application import app


@app.route('/run_log/batch/add', methods=['POST'])
def add_batch_run_log():
    """
    :return:
    """
    print(request.get_json())
    try:
        RunLogAPI.add_batch_run_log(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True})


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





