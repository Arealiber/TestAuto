from datetime import datetime
import pytz
import pandas as pd


tz = pytz.timezone(pytz.country_timezones('cn')[0])


def utc_to_shanghai_timezone(time_in):
    """
    utc时间转上海时区时间
    :param time_in: datetime格式的utc时间
    :return: datetime时间的本地时区时间
    """
    if time_in:
        time_utc = time_in.replace(tzinfo=pytz.timezone('UTC'))
        time_local = time_utc.astimezone(pytz.timezone('Asia/Shanghai'))
        return time_local
    return time_in


def shanghai_to_utc_timezone(time_in):
    """
    上海时区时间转utc时间
    :param time_in: datetime格式的utc时间
    :return: datetime时间的本地时区时间
    """
    if time_in:
        time_utc = tz.localize(time_in)
        time_local = time_utc.astimezone(pytz.timezone('UTC'))
        return time_local
    return time_in


def get_function_of_data(use_case_report_list):
    all_report_data = {}
    single_report_data = {}
    for use_case_report in use_case_report_list:
        function_id = use_case_report.get('function_id')
        if all_report_data.get(function_id, None):
            single_report_data = all_report_data[function_id]
            single_report_data['run_count'] += use_case_report['run_count']
            single_report_data['success_count'] += use_case_report['success_count']
            single_report_data['fail_count'] += use_case_report['fail_count']
            if single_report_data['max_time'] < use_case_report['max_time']:
                single_report_data['max_time'] = use_case_report['max_time']
            single_report_data['sum_time'] += use_case_report.get('sum_time')
        else:
            if single_report_data:
                single_report_data = {}
            single_report_data['function_id'] = function_id
            single_report_data['run_count'] = use_case_report['run_count']
            single_report_data['success_count'] = use_case_report['success_count']
            single_report_data['fail_count'] = use_case_report['fail_count']
            single_report_data['max_time'] = use_case_report['max_time']
            single_report_data['sum_time'] = use_case_report['sum_time']
            single_report_data['create_time'] = tz.localize(use_case_report['create_time'])
            all_report_data[function_id] = single_report_data
    all_report_list = all_report_data.values()
    for report_data in all_report_list:
        average_time = report_data['sum_time'] / report_data['run_count']
        pass_rate = report_data['success_count'] / report_data['run_count']
        report_data['average_time'] = average_time
        report_data['pass_rate'] = pass_rate
        if report_data.get('create_time', None):
            report_data.pop('create_time')
    return list(all_report_list)


def get_line_of_data(report_data_list, time_format='%Y%m%d', filter_line_name='business_line_id'):
    all_report_data = {}
    single_report_data = {}
    filter_line_str = filter_line_name
    for use_case_report in report_data_list:
        filter_line_id = use_case_report.get(filter_line_str)
        create_time = use_case_report.get('create_time').strftime(time_format)

        key = str(filter_line_id) + create_time
        if all_report_data.get(key, None):
            single_report_data = all_report_data[key]
            single_report_data['run_count'] += use_case_report['run_count']
            single_report_data['success_count'] += use_case_report['success_count']
            single_report_data['fail_count'] += use_case_report['fail_count']
            if single_report_data['max_time'] < use_case_report['max_time']:
                single_report_data['max_time'] = use_case_report['max_time']
            single_report_data['sum_time'] += use_case_report.get('sum_time')
        else:
            if single_report_data:
                single_report_data = {}
            single_report_data[filter_line_str] = filter_line_id
            single_report_data['run_count'] = use_case_report['run_count']
            single_report_data['success_count'] = use_case_report['success_count']
            single_report_data['fail_count'] = use_case_report['fail_count']
            single_report_data['max_time'] = use_case_report['max_time']
            single_report_data['sum_time'] = use_case_report['sum_time']
            single_report_data['create_time'] = tz.localize(use_case_report['create_time'])
            single_report_data['business_name'] = use_case_report['business_name']
            single_report_data['system_name'] = use_case_report['system_name']
            all_report_data[key] = single_report_data
    all_report_list = all_report_data.values()

    for report_data in all_report_list:
        average_time = report_data['sum_time'] / report_data['run_count']
        pass_rate = round(report_data['success_count'] / report_data['run_count'], 3)
        report_data['average_time'] = average_time
        report_data['pass_rate'] = pass_rate
    return list(all_report_list)









