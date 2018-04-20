# -*- coding:utf-8 -*-
import time
from flask import request, jsonify
from application.config.default import *
from application import app
from application.api import run_log as RunLogAPI

current_time = time.strftime(rebuild_run_log_table_time)


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


