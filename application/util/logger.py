import requests
import time
from concurrent.futures import ThreadPoolExecutor


# 多线程执行器
executor = ThreadPoolExecutor()

# log上报url
LOG_REPORT_URL = 'http://logreport.huishoubao.com/autotest/?{0}'

# log内容
LOG_FORMAT_STRING = '{0}={1}={2}={3}={4}={5}={6}={7}={8}'

# 所在节点ID
HOSTNAME = '10.29.20.12'


def send_log(url_param_string):
    """
    将log上报
    :param url_param_string:        log内容
    :return:
    """
    url = LOG_REPORT_URL.format(url_param_string)
    requests.get(url)


def log(url_param_string):
    """
    将log排入线程池上报
    :param url_param_string:        log内容
    :return:
    """
    executor.submit(send_log, url_param_string)


def request_log(target_name, target_id, interface, code, cost_time):
    """
    常规上报（调用成功或错误或超时均上报，内部错误不上报）
    全部传入param都为string
    :param target_name:             被调方ID, 目标服务名
    :param target_id:               被调方节点ID, 暂时用目标服务名
    :param interface:               方法ID, 接口名
    :param code:                    返回码, 0表示成功，非0失败
    :param cost_time:               耗时, 单位毫秒
    :return:
    """
    url_param_string = LOG_FORMAT_STRING.format(
        '1',
        str(int(time.time())),
        'InspectSys',
        HOSTNAME,
        target_name,
        target_id,
        interface,
        code,
        cost_time
    )
    log(url_param_string)


def exception_log(target_name, error_message, interface, code, cost_time):
    """
    异常上报（错误和异常上报，内部错误也上报，成功不上报）
    全部传入param都为string
    :param target_name:            被调方ID, 目标服务名
    :param error_message:          错误信息
    :param interface:              方法ID, 接口名
    :param code:                   返回码, 0表示成功，非0失败
    :param cost_time:              耗时, 单位毫秒
    :return:
    """
    url_param_string = LOG_FORMAT_STRING.format(
        '8',
        str(int(time.time())),
        'InspectSys',
        HOSTNAME,
        target_name,
        error_message,
        interface,
        code,
        cost_time
    )
    log(url_param_string)
