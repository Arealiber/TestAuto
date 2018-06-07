import requests
import time
import socket
from datetime import datetime
from dateutil.rrule import rrule, DAILY
from functools import wraps
from flask import session, request, redirect, jsonify
from requests.exceptions import ConnectionError, ConnectTimeout
import pandas as pd

from application import app

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
        if user or app.config['DEBUG']:
            return f(*args, **kwargs)
        else:
            if 'login_token' in request.args and 'user_id' in request.args:
                login_token = request.args.get('login_token')
                user_id = request.args.get('user_id')
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
                    json_response = r.json()
                    if json_response['body']['ret'] == '0':
                        session['user_id'] = user_id
                        session['timestamp'] = str(int(time.time()))
                        session['real_name'] = json_response['body']['data']['user_info']['real_name']
                        return f(*args, **kwargs)
                    else:
                        return jsonify({'success': False, 'error': '登陆失败'})
                except ConnectTimeout:
                    # 链接超时
                    pass
                except ConnectionError:
                    # 链接错误
                    pass
                except:
                    # 其他错误
                    pass
            else:
                return redirect('http://api-amc.huishoubao.com.cn/login?system_id={0}&jump_url={1}'.format(app.config['SYSTEM_ID'], request.url))

    return decorated_function


def localhost_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        local_host_ip = request.remote_addr
        if not local_host_ip == '127.0.0.1':
            return jsonify({'success': False, 'error': 'you have to been called by localhost'})
        return func(*args, **kwargs)
    return wrapper


def report_data_manager(data_list, time_format='%Y/%m/%d'):
    report_business_list = []
    end_time = None
    start_time = None
    for report_info in data_list:
        business_name = report_info.get('business_name')
        if business_name not in report_business_list:
            report_business_list.append(business_name)
        temp_time = report_info.get('create_time')
        if end_time is None or end_time < temp_time:
            end_time = temp_time
        if not start_time or start_time > temp_time:
            start_time = temp_time
    report_time_list = [dt.strftime(time_format) for dt in rrule(DAILY,
                                                                 dtstart=start_time,
                                                                 until=end_time)]
    if report_time_list:
        report_time_list.append(end_time.strftime(time_format))
    else:
        report_time_list=[end_time.strftime(time_format)]
    temp_time = []
    for report_time in report_time_list :
        if report_time not in temp_time:
            temp_time.append(report_time)
    report_time_list = temp_time
    report_df = pd.DataFrame(columns=report_time_list, index=report_business_list)
    for report_info in data_list:
        create_time = report_info.get('create_time').strftime(time_format)
        business_name = report_info.get('business_name')
        report_df[create_time][business_name] = report_info.get('pass_rate')*100
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


