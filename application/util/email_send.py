# -*- coding:utf-8 -*-
import requests
import time
import html
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from application.util import get_line_of_data
from application.api import report as ReportAPI
from application.api import menutree as MenuTreeAPI
from application.config.default import *


def email_send(**kwargs):
    """
    发送邮件
    :param kwargs:    所需参数，包括收件人/邮件标题/邮件内容
    :return:          成功True， 失败False
    """
    json_data = {
        'head': {
            'version': '0.01',
            'msgtype': 'request',
            'interface': 'account1',
            'remark': ''
        },
        'params': {
            'system': 'HSB',
            'time': int(time.time()),
            'address': kwargs['address'],
            'subject': kwargs['title'],
            'body': kwargs['body']
        }
    }
    print(kwargs.get('str_url'))
    str_url = kwargs.get('str_url')
    res = requests.post(str_url, json=json_data, proxies=kwargs['proxies'])
    print(res, res.content)
    return True


def get_send_body():
    kwarg = dict()
    now_time_point = datetime.now()
    to_time_point = now_time_point + timedelta(days=1)
    from_time_point = now_time_point - relativedelta(months=1)
    kwarg['to_time'] = to_time_point.strftime(DAY_TIME_FMT)
    kwarg['from_time'] = from_time_point.strftime(DAY_TIME_FMT)
    report_info_list = ReportAPI.get_day_report_info(**kwarg)
    menu_tree_info = MenuTreeAPI.query_line_relation()
    for report_info in report_info_list:
        function_id = report_info.get('function_id')
        report_info.update(menu_tree_info[function_id])
    report_info_list = get_line_of_data(report_info_list, filter_line_name='system_line_id')
    return report_info_list


def get_html_data():
    inline_css = {
        'class1': 'color:#00FF00;',
        'class2': 'color:#FF0000;',
        'class3': 'color:#FFFF00;',
    }

    b = html._html5
    t = b.table(border='1')
    r = t.tr()
    r.td('column 1', style=inline_css['class1'])
    r.td('column 2', style=inline_css['class2'])
    r.td('column 3', style=inline_css['class3'])
    return b


if __name__ == '__main__':
    kwargs = dict()
    kwargs['str_url'] = 'http://push.huishoubao.com/email-interface'
    kwargs['address'] = {'lichengbo': 'lichengbo@huishoubao.com.cn'}
    kwargs['title'] = '自动化巡检报表'
    with open('D:\\AutoTest\\1.html', encoding="utf-8") as f:
        data = f.read()
    kwargs['body'] = '测试'
    kwargs['proxies'] = {
        'http': '119.29.141.207'
    }
    email_send(**kwargs)





