from datetime import datetime
import pytz


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
        time_utc = time_in.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
        time_local = time_utc.astimezone(pytz.timezone('UTC'))
        return time_local
    return time_in


def add_report_data_calculate(use_case_report_list):
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
            single_report_data['create_time'] = use_case_report['create_time']
            all_report_data[function_id] = single_report_data
    all_report_list = all_report_data.values()
    for report_data in all_report_list:
        average_time = report_data['sum_time'] / report_data['run_count']
        pass_rate = report_data['success_count'] / report_data['run_count']
        report_data['average_time'] = average_time
        report_data['pass_rate'] = pass_rate
    return list(all_report_list)


def get_business_of_data(report_data_list):
    all_report_data = {}
    single_report_data = {}
    for use_case_report in report_data_list:
        business_line_id = use_case_report.get('business_line_id')
        create_time = use_case_report.get('create_time').strftime('%Y%m%d')

        key = str(business_line_id) + create_time
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
            single_report_data['business_line_id'] = business_line_id
            single_report_data['run_count'] = use_case_report['run_count']
            single_report_data['success_count'] = use_case_report['success_count']
            single_report_data['fail_count'] = use_case_report['fail_count']
            single_report_data['max_time'] = use_case_report['max_time']
            single_report_data['sum_time'] = use_case_report['sum_time']
            single_report_data['create_time'] = use_case_report['create_time']
            all_report_data[key] = single_report_data
    all_report_list = all_report_data.values()

    for report_data in all_report_list:
        average_time = report_data['sum_time'] / report_data['run_count']
        pass_rate = report_data['success_count'] / report_data['run_count']
        report_data['average_time'] = average_time
        report_data['pass_rate'] = pass_rate
    return list(all_report_list)







