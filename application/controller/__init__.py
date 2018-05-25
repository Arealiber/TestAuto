import requests
import time

from functools import wraps
from flask import session, request, redirect, url_for

from application import app

USER_INFO_URL = 'http://api-amc.huishoubao.com.cn/loginuserinfo'


def cur_user():
    return session['user_id'] if 'user_id' in session else None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = cur_user()
        if user:
            return f(*args, **kwargs)
        else:
            if 'login_toke' in request.args and 'user_id' in request.args:
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
                        "login_system_id": "1"
                    }
                }
                try:
                    r = requests.post(USER_INFO_URL, json=params)
                    json_response = r.json()
                    if json_response['body']['ret'] == '0':
                        session['user_id'] = user_id
                        session['timestamp'] = str(int(time.time()))
                    else:
                        return redirect('http://api-amc.huishoubao.com.cn/login?system_id={0}&jump_url=urlencode({1})'.format(app.config['SYSTEM_ID'], url_for('index')))
                except:
                    pass
            else:
                return redirect('http://api-amc.huishoubao.com.cn/login?system_id={0}&jump_url=urlencode({1})'.format(app.config['SYSTEM_ID'], request.url))

    return decorated_function
