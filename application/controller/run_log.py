# -*- coding:utf-8 -*-
from datetime import datetime
from application.config.default import QUERY_TIME_FMT
from flask import request, jsonify
from application.api import run_log as RunLogAPI
from application.api import use_case as UseCaseAPI
from application.api import interface as InterfaceAPI
from application.api import batch as BatchAPI
from application import app
from application.util import *


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
    from_time = request.get_json().get('from_time', None)
    to_time = request.get_json().get('to_time', None)
    if from_time:
        from_time = shanghai_to_utc_timezone(datetime.strptime(from_time, QUERY_TIME_FMT))
        request.get_json().update({"from_time": from_time.strftime(QUERY_TIME_FMT)})
    if to_time:
        to_time = shanghai_to_utc_timezone(datetime.strptime(to_time, QUERY_TIME_FMT))
        request.get_json().update({"to_time": to_time.strftime(QUERY_TIME_FMT)})
    param_json = request.get_json()
    page_index = int(param_json.pop('pageIndex')) if 'pageIndex' in param_json else 1
    page_size = int(param_json.pop('pageSize')) if 'pageSize' in param_json else 10
    try:
        result = RunLogAPI.get_multi_batch_run_log_info(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    result = result[(page_index - 1) * page_size:page_index * page_size]
    for batch_run_log_dict in result:
        batch_run_log = BatchAPI.get_batch(id=batch_run_log_dict.get('batch_id'))
        if batch_run_log:
            batch_run_log = batch_run_log[0]
        else:
            continue
        batch_run_log_dict['batch_name'] = batch_run_log.get('batch_name')
        start_time = utc_to_shanghai_timezone(batch_run_log_dict.get('start_time'))
        end_time = utc_to_shanghai_timezone(batch_run_log_dict.get('end_time'))
        batch_run_log_dict.update({'start_time': datetime.strftime(start_time, QUERY_TIME_FMT)})
        if end_time:
            batch_run_log_dict.update({'end_time': datetime.strftime(end_time, QUERY_TIME_FMT)})
    return jsonify({'success': True, 'res': result})


@app.route('/run_log/batch/count', methods=['POST'])
def get_batch_run_log_count():
    """
    :return:
    """
    from_time = request.get_json().get('from_time', None)
    to_time = request.get_json().get('to_time', None)
    if from_time:
        from_time = shanghai_to_utc_timezone(datetime.strptime(from_time, QUERY_TIME_FMT))
        request.get_json().update({"from_time": from_time.strftime(QUERY_TIME_FMT)})
    if to_time:
        to_time = shanghai_to_utc_timezone(datetime.strptime(to_time, QUERY_TIME_FMT))
        request.get_json().update({"to_time": to_time.strftime(QUERY_TIME_FMT)})
    try:
        result = RunLogAPI.get_batch_run_log_count(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/run_log/use_case/add', methods=['POST'])
def add_use_case_run_log():
    """
    :return:
    """
    try:
        RunLogAPI.add_use_case_run_log(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True})


@app.route('/run_log/use_case/count', methods=['POST'])
def get_use_case_run_log_count():
    """
    :return:
    """
    from_time = request.get_json().get('from_time', None)
    to_time = request.get_json().get('to_time', None)
    if from_time:
        from_time = shanghai_to_utc_timezone(datetime.strptime(from_time, QUERY_TIME_FMT))
        request.get_json().update({"from_time": from_time.strftime(QUERY_TIME_FMT)})
    if to_time:
        to_time = shanghai_to_utc_timezone(datetime.strptime(to_time, QUERY_TIME_FMT))
        request.get_json().update({"to_time": to_time.strftime(QUERY_TIME_FMT)})
    try:
        result = RunLogAPI.get_use_case_run_log_count(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/run_log/use_case/info', methods=['POST'])
def get_use_case_run_log():
    """
    :return:
    """
    from_time = request.get_json().get('from_time', None)
    to_time = request.get_json().get('to_time', None)
    if from_time:
        from_time = shanghai_to_utc_timezone(datetime.strptime(from_time, QUERY_TIME_FMT))
        request.get_json().update({"from_time": from_time.strftime(QUERY_TIME_FMT)})
    if to_time:
        to_time = shanghai_to_utc_timezone(datetime.strptime(to_time, QUERY_TIME_FMT))
        request.get_json().update({"to_time": to_time.strftime(QUERY_TIME_FMT)})
    param_json = request.get_json()
    page_index = int(param_json.pop('pageIndex')) if 'pageIndex' in param_json else 1
    page_size = int(param_json.pop('pageSize')) if 'pageSize' in param_json else 10

    try:
        result = RunLogAPI.get_use_case_run_log(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    result = result[(page_index - 1) * page_size:page_index * page_size]
    for use_case_run_log_dict in result:
        use_case_id = use_case_run_log_dict.get('use_case_id')
        use_case_info = UseCaseAPI.get_single_use_case(use_case_id)
        use_case_name = use_case_info.get('use_case_name')
        use_case_run_log_dict.update({'use_case_name': use_case_name})
        start_time = utc_to_shanghai_timezone(use_case_run_log_dict.get('start_time'))
        end_time = utc_to_shanghai_timezone(use_case_run_log_dict.get('end_time'))
        use_case_run_log_dict.update({'start_time': datetime.strftime(start_time, QUERY_TIME_FMT)})
        if end_time:
            use_case_run_log_dict.update({'end_time': datetime.strftime(end_time, QUERY_TIME_FMT)})
    return jsonify({'success': True, 'res': result})


@app.route('/run_log/use_case/add', methods=['POST'])
def add_interface_run_log():
    """
    :return:
    """
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
    from_time = request.get_json().get('from_time', None)
    to_time = request.get_json().get('to_time', None)
    if from_time:
        from_time = shanghai_to_utc_timezone(datetime.strptime(from_time, QUERY_TIME_FMT))
        request.get_json().update({"from_time": from_time.strftime(QUERY_TIME_FMT)})
    if to_time:
        to_time = shanghai_to_utc_timezone(datetime.strptime(to_time, QUERY_TIME_FMT))
        request.get_json().update({"to_time": to_time.strftime(QUERY_TIME_FMT)})
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
        start_time = utc_to_shanghai_timezone(interface_run_log_dict.get('start_time'))
        end_time = utc_to_shanghai_timezone(interface_run_log_dict.get('end_time'))
        interface_run_log_dict.update({'start_time': datetime.strftime(start_time, QUERY_TIME_FMT)})
        if end_time:
            interface_run_log_dict.update({'end_time': datetime.strftime(end_time, QUERY_TIME_FMT)})
    return jsonify({'success': True, 'res': result})
