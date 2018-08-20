import requests
import time
import socket
import os
from functools import wraps
from flask import session, request, redirect, jsonify
from requests.exceptions import ConnectionError, ConnectTimeout
import pandas as pd

from application import app
from application.util import g_DNS
if not app.config['DEBUG']:
    from application.util import logger as Logger

USER_INFO_URL = 'http://api-amc.huishoubao.com.cn/loginuserinfo'


if not app.config['DEBUG']:
    DNS = {'api-amc.huishoubao.com.cn': '139.199.164.232'}
else:
    DNS = {}

old_getaddrinfo = socket.getaddrinfo


def new_getaddrinfo(*args):
    result = old_getaddrinfo(*args)[0]
    dns_result = result[4]
    if args[0] in DNS:
        dns_result = (DNS[args[0]], dns_result[1])
    modified_result = [(result[0], result[1], result[2], result[3], dns_result)]
    return modified_result


socket.getaddrinfo = new_getaddrinfo


def cur_user():
    return session['user_id'] if 'user_id' in session else None


def user_real_name():
    return session['real_name']


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = cur_user()
        if user:
            return f(*args, **kwargs)
        elif app.config['DEBUG']:
            session['user_id'] = app.config['SYSTEM_ID']
            session['timestamp'] = str(int(time.time()))
            session['real_name'] = '管理员'
            return f(*args, **kwargs)
        else:
            if ('login_token' in request.args and 'user_id' in request.args) or \
                    (request.get_json() and 'login_token' in request.get_json() and 'user_id' in request.get_json()):

                login_token = request.args.get('login_token', None) or request.get_json().get('login_token', None)
                user_id = request.args.get('user_id', None) or request.get_json().get('user_id', None)
                if login_token and user_id is not None and check_login(user_id, login_token):
                    return f(*args, **kwargs)
                else:
                    return jsonify({'success': False, 'res': '登陆失败'})
            else:
                return redirect('http://api-amc.huishoubao.com.cn/login?system_id={0}&jump_url={1}'
                                .format(app.config['SYSTEM_ID'], request.url))

    return decorated_function


def check_login(user_id, login_token):
    params = {
        "head": {
            "interface": "loginuserinfo",
            "msgtype": "request",
            "remark": "",
            "version": "0.01"
        },
        "params": {
            "login_token": login_token,
            "login_user_id": user_id,
            "login_system_id": app.config['SYSTEM_ID']
        }
    }
    try:
        r = requests.post(USER_INFO_URL, json=params, timeout=5)
        print(r.json())
        json_response = r.json()
        if json_response['body']['ret'] == '0':
            session['user_id'] = user_id
            session['timestamp'] = str(int(time.time()))
            session['real_name'] = json_response['body']['data']['user_info']['real_name']
            return True
        else:
            return False
    except ConnectTimeout:
        # 链接超时
        pass
    except ConnectionError:
        # 链接错误
        pass
    except:
        # 其他错误
        pass


def localhost_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        local_host_ip = request.remote_addr
        if not local_host_ip == '127.0.0.1':
            return jsonify({'success': False, 'error': 'you have to been called by localhost'})
        return func(*args, **kwargs)
    return wrapper


def del_g_dns(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        cur_pid = os.getpid()
        g_dns_dict = g_DNS.get_dns()
        Logger.info_log(g_dns_dict)
        if cur_pid in g_dns_dict:
            del g_dns_dict[cur_pid]
        Logger.info_log(g_dns_dict)
        return ret
    return wrapper


def report_data_manager(data_list, time_format='%Y/%m/%d'):
    report_business_list = []
    end_time = None
    start_time = None
    temp_time_report = []
    for report_info in data_list:
        business_name = report_info.get('business_name')
        if business_name not in report_business_list:
            report_business_list.append(business_name)
        temp_time = report_info.get('create_time')
        if temp_time not in temp_time_report:
            temp_time_report.append(temp_time)
        if end_time is None or end_time < temp_time:
            end_time = temp_time
        if not start_time or start_time > temp_time:
            start_time = temp_time
    temp_time_report = list(set([temp_time.strftime(time_format) for temp_time in sorted(temp_time_report)]))
    temp_time_report = sorted(temp_time_report)
    report_time_list = temp_time_report
    report_df = pd.DataFrame(columns=report_time_list, index=report_business_list)
    for report_info in data_list:
        create_time = report_info.get('create_time').strftime(time_format)
        business_name = report_info.get('business_name')
        report_df.loc[business_name, [create_time]] = report_info.get('pass_rate')*100
    report_df = report_df.fillna(-1)
    datasets = []
    for i in range(len(report_df)):
        datasets.append({
            'label': report_business_list[i],
            'data': list(report_df.iloc[i])
        })
    if time_format == '%W':
        report_time_list = ['第{0}周'.format(report_time) for report_time in report_time_list]
    chartist_data = {
        'type': 'line',
        'data': {
            'labels': report_time_list,
            'datasets': datasets
        },
        'options': {
            'scales': {
                'yAxes': [{
                    'ticks': {
                        'min': 0,
                        'max': 100
                    }
                }]
            }
        }
    }
    return chartist_data


