import requests
import time
import html


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
    str_url = kwargs.get('str_url')
    requests.post(str_url, json=json_data, proxies=kwargs['proxies'])
    return True


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
    kwargs['body'] = data
    kwargs['proxies'] = {
        'http': '119.29.141.207'
    }
    email_send(**kwargs)





