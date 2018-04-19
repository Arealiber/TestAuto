# -*- coding:utf-8 -*-
import time, importlib
from flask import request, jsonify
from application import app
from application.api import run_log as RunLogAPI

current_time = time.strftime('%Y%m%M')


if RunLogAPI.current_time != current_time:
    RunLogAPI, = RunLogAPI.reload_import_module('application.api', run_log='run_log')


@app.route('/run_log/add', methods=['POST'])
def get_use_case_run_log():
    """
    :return:
    """
    try:
        RunLogAPI.add_use_case_run_log(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True})


