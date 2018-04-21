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

