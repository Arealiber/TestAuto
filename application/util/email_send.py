# -*- coding:utf-8 -*-
import os
import time
import requests
if __name__ != '__main__':
    from datetime import datetime, timedelta
    from application.util import get_line_of_data
    from application.api import report as ReportAPI
    from application.api import menutree as MenuTreeAPI
    from application.config.default import *


def email_send(**kwargs):
    """
    发送邮件
    发件人：attc@huishoubao.com.cn 密码：Att123456
    :param kwargs:    所需参数，包括收件人/邮件标题/邮件内容
    :return:          成功True， 失败False
    """
    json_data = {
        'head': {
            'version': '0.01',
            'msgtype': 'request',
            'interface': 'account5',
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
    str_url = kwargs.get('str_url')
    r = requests.post(str_url, json=json_data, proxies=kwargs.get('proxies', None))
    if r.status_code == 200:
        return 0
    else:
        return r.text


def get_send_body():
    kwarg = dict()
    now_time_point = datetime.now()
    to_time_point = now_time_point
    from_time_point = now_time_point - timedelta(days=1)
    kwarg['to_time'] = to_time_point.strftime(DAY_TIME_FMT)
    kwarg['from_time'] = from_time_point.strftime(DAY_TIME_FMT)
    report_info_list = ReportAPI.get_day_report_info(**kwarg)
    menu_tree_info = MenuTreeAPI.query_line_relation()
    for report_info in report_info_list:
        function_id = report_info.get('function_id')
        report_info.update(menu_tree_info[function_id])
    report_info_list = get_line_of_data(report_info_list, filter_line_name='system_line_id')
    cur_wk_path = os.path.join(web_root, 'static', 'email_template.html')

    with open(cur_wk_path, 'r+', encoding="utf-8") as fp:
        fp_data = fp.read()
        fp_data = fp_data.format(now_time_point.strftime('%Y/%m/%d %H:%M'))
        index = fp_data.find('<tbody>')
        before_insert_data = fp_data[:index]
        after_insert_data = fp_data[index:]
        for report_data in report_info_list:
            html_tmp = '<tr>' \
                       '<td role="row">{0}</td>' \
                       '<td role="row">{1}</td>' \
                       '<td role="row">{2}</td>' \
                       '<td role="row">{3}</td>' \
                       '<td role="row">{4}</td>' \
                       '<td role="row">{5}</td>' \
                       '<td role="row">{6}</td>' \
                       '<td role="row">{7}</td>' \
                       '</tr>'
            create_time = report_data['create_time'].strftime('%Y-%m-%d')
            before_insert_data += html_tmp.format(report_data['business_name'], report_data['system_name'],
                                                  report_data['run_count'], report_data['fail_count'],
                                                  round(report_data['pass_rate']*100, 3),
                                                  float('%.3f' % report_data['average_time']),
                                                  float('%.3f' % report_data['max_time']), create_time)

    return before_insert_data + after_insert_data


if __name__ == '__main__':
    kwargs = dict()
    kwargs['str_url'] = 'http://push.huanjixia.com/email-interface'
    kwargs['address'] = {'lichengbo': 'lichengbo@huishoubao.com.cn'}
    kwargs['title'] = '自动化巡检报表'
    with open('D:\\AutoTest\\email_template.html', encoding="utf-8") as f:
        data = f.read()
    kwargs['body'] = '测试'
    kwargs['proxies'] = {
        'http': '119.29.141.207'
    }
    email_send(**kwargs)





