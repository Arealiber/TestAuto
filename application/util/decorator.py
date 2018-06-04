# -*- coding:utf-8 -*-
from datetime import datetime
from application.config.default import *
from dateutil.rrule import rrule, DAILY
from functools import wraps
from flask import make_response


# 处理日志模块对于分表和按时间查询参数的装饰器
def run_log_table_decorator(func):
    def wrapper(**kwargs):
        """
        对被装饰的函数的参数进行类型处理
        :param kwargs:
            from_time和to_time表示起止时间，table_name_fix_lst用于存储表格名称后缀
        :return:
        """
        fmt_str = (datetime.strftime(datetime.utcnow(), QUERY_TIME_FMT))
        if not('from_time' in kwargs or 'to_time' in kwargs):
            kwargs.update({'table_name_fix_lst': [fmt_str[:CONSTANT_LEN]]})
        else:
            from_time = kwargs.get('from_time').strip() if kwargs.get('from_time') else None
            to_time = kwargs.get('to_time').strip() if kwargs.get('to_time') else fmt_str.strip()
            table_to_time = to_time[:CONSTANT_LEN]
            if not from_time:
                table_from_time = table_to_time
            else:
                table_from_time = from_time[:CONSTANT_LEN]
            dt_table_from_time, dt_table_to_time = multi_strptime(table_from_time, table_to_time,
                                                                  str_format=TABLE_TIME_FMT)
            table_name_fix_lst = [dt.strftime(TABLE_TIME_FMT) for dt in rrule(DAILY,
                                                                              dtstart=dt_table_from_time,
                                                                              until=dt_table_to_time)]
            dt_from_time, dt_to_time = multi_strptime(from_time, to_time)
            kwargs.update({
                'table_name_fix_lst': table_name_fix_lst,
                'from_time': dt_from_time,
                'to_time': dt_to_time
            })
        return func(**kwargs)
    return wrapper


# 批量把字符串格式生成datetime格式
def multi_strptime(*args, str_format=QUERY_TIME_FMT):
    dt_time = []
    for dt_arg in args:
        if dt_arg is None:
            dt_time.append(None)
            continue
        dt_time.append(datetime.strptime(dt_arg, str_format))
    return tuple(dt_time)


# 去掉浏览器缓存装饰器
def no_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    return wrapper


def report_table_decorator(func):
    @wraps(func)
    def wrapper(**kwargs):
        fmt_str = (datetime.strftime(datetime.utcnow(), TABLE_FMT))
        kwargs.update({'table_name': [fmt_str]})  # 按年分表
        return func(**kwargs)
    return wrapper


# def add_report_table_decorator(report_func):
#     @wraps(report_func)
#     def wrapper(**kwargs):
#         fmt_str = (datetime.strftime(datetime.utcnow(), TABLE_FMT))
#         kwargs.update({'table_name': [fmt_str]})   # 按年分表
#         use_case_report_list = report_func(**kwargs)
#         all_report_data = {}
#         single_report_data = {}
#         for use_case_report in use_case_report_list:
#             function_id = use_case_report.get('function_id')
#             if all_report_data.get(function_id, None):
#                 single_report_data = all_report_data[function_id]
#                 single_report_data['run_count'] += use_case_report['run_count']
#                 single_report_data['success_count'] += use_case_report['success_count']
#                 single_report_data['fail_count'] += use_case_report['fail_count']
#                 if single_report_data['max_time'] < use_case_report['max_time']:
#                     single_report_data['max_time'] = use_case_report['max_time']
#                 single_report_data['sum_time'] += use_case_report.get('sum_time')
#             else:
#                 if single_report_data:
#                     single_report_data = {}
#                 single_report_data['function_id'] = function_id
#                 single_report_data['run_count'] = use_case_report['run_count']
#                 single_report_data['success_count'] = use_case_report['success_count']
#                 single_report_data['fail_count'] = use_case_report['fail_count']
#                 single_report_data['max_time'] = use_case_report['max_time']
#                 single_report_data['sum_time'] = use_case_report['sum_time']
#                 single_report_data['create_time'] = use_case_report['create_time']
#                 all_report_data[function_id] = single_report_data
#         all_report_list = all_report_data.values()
#         for report_data in all_report_list:
#             average_time = report_data['sum_time'] / report_data['run_count']
#             pass_rate = report_data['success_count'] / report_data['run_count']
#             report_data['average_time'] = average_time
#             report_data['pass_rate'] = pass_rate
#         return list(all_report_list)
#     return wrapper
#













