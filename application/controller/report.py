# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from flask import request, jsonify
from application.api import report as ReportAPI
from application.api import menutree as MenuTreeAPI
from application.api import run_log as RunLogAPI
from application.api import use_case as UseCaseAPI
from application import app
from application.util.exception import try_except
from application.controller import login_required
from application.config.default import *
import json
from pprint import pprint


@app.route('/report/minutes_report/add', methods=['GET'])
@try_except
# @login_required
def add_minutes_report():
    """
    :return:
    """
    now_time_point = datetime.utcnow()
    before_time_point = now_time_point - timedelta(minutes=MIN_TIME_LENGTH)
    to_time = now_time_point.strftime(QUERY_TIME_FMT)
    from_time = before_time_point.strftime(QUERY_TIME_FMT)

    use_case_run_log_list = RunLogAPI.get_use_case_run_log(from_time=from_time, to_time=to_time)
    use_case_id_list = list(set([use_case_run_log.get('use_case_id') for use_case_run_log in use_case_run_log_list]))
    use_case_info_dict = UseCaseAPI.get_multi_use_case(use_case_id_list)

    all_report_data = {}
    single_report_data = {}
    for use_case_run_log in use_case_run_log_list:
        use_case_id = use_case_run_log.get('use_case_id')
        if all_report_data.get(use_case_id, None):
            single_report_data = all_report_data[use_case_id]
            single_report_data['run_count'] += 1
            if use_case_run_log.get('is_pass'):
                single_report_data['success_count'] += 1
            else:
                single_report_data['fail_count'] += 1
            single_report_data['sum_time'] += use_case_run_log.get('cost_time')
            cost_time = use_case_run_log.get('cost_time')
            if single_report_data['max_time'] < cost_time:
                single_report_data['max_time'] = cost_time
        else:
            if single_report_data:
                single_report_data = {}
            single_report_data['use_case_id'] = use_case_id
            single_report_data['run_count'] = 1
            if use_case_run_log.get('is_pass'):
                single_report_data['success_count'] = 1
                single_report_data['fail_count'] = 0
            else:
                single_report_data['success_count'] = 0
                single_report_data['fail_count'] = 1
            single_report_data['sum_time'] = use_case_run_log.get('cost_time')
            single_report_data['max_time'] = use_case_run_log.get('cost_time')
            single_report_data['function_id'] = use_case_info_dict[use_case_id].get('function_id')
            all_report_data[use_case_id] = single_report_data
    all_report_list = list(all_report_data.values())
    for report_data in all_report_list:
        average_time = report_data['sum_time'] / report_data['run_count']
        pass_rate = report_data['success_count'] / report_data['run_count']
        report_data['average_time'] = average_time
        report_data['pass_rate'] = pass_rate
        report_data.pop('sum_time')
        ReportAPI.add_minutes_report(**report_data)
    return jsonify({'success': True})





