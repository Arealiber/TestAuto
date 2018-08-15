import json
import timeit
import time
import sys
import traceback
import re
import socket
import html
import requests
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime
from requests.exceptions import ConnectionError, ConnectTimeout

from application import app
from application.util import encryption as Encryption
from application.util import parameter as ParameterUtil
from application.api import run_log as RunLogAPI
from application.api import interface as InterfaceAPI
from application.api import parameter as ParameterAPI
from application.api import batch as BatchAPI
from application.api import use_case as UseCaseAPI
from application.api import encryption as EncryptionAPI
from application.api import environment as EnvironmentAPI
from application.util.exception import try_except
from application.util import g_DNS

if not app.config['DEBUG']:
    from application.util import logger as LOGGER
else:
    from application.util import LocalLogger as LOGGER


# 多进程执行器
executor = ThreadPoolExecutor(max_workers=8)

old_getaddrinfo = socket.getaddrinfo


def new_getaddrinfo(*args):
    url = args[0]
    cur_pid = os.getpid()
    g_dns_dict = g_DNS.get_dns()
    LOGGER.info_log('dns内容：{0},url:{1}'.format(g_dns_dict, url))
    if cur_pid in g_dns_dict and url in g_dns_dict[cur_pid].keys():
        new_dns = g_dns_dict[cur_pid]

        local_args = ('www.huishoubao.com.cn', args[1], args[2], args[3])
        result = old_getaddrinfo(*local_args)[0]
        dns_result = result[4]
        try:
            dns_result = (new_dns[url], dns_result[1])
        except KeyError as e:
            LOGGER.info_log('键值{0}不存在，DNS_CACHE:{1}'.format(str(e), new_dns))
            raise

        modified_result = [(result[0], result[1], result[2], result[3], dns_result)]
        return modified_result
    else:
        result = old_getaddrinfo(*args)
        return result


socket.getaddrinfo = new_getaddrinfo


@try_except
def interface_log_insert(interface_log_dict):
    """
    记录接口请求日志
    :param interface_log_dict:      接口请求信息
    """
    interface_end_time = datetime.utcnow()
    interface_stop = interface_log_dict['interface_stop'] if 'interface_stop' in interface_log_dict else timeit.default_timer()

    RunLogAPI.add_interface_run_log(**{
        'use_case_run_log_id': interface_log_dict['use_case_run_log_id'],
        'interface_id': interface_log_dict['interface_id'],
        'is_pass': interface_log_dict['is_pass'],
        'cost_time': interface_stop - interface_log_dict['interface_start'] if 'interface_start' in interface_log_dict else 0,
        'start_time': interface_log_dict['interface_start_time'],
        'end_time': interface_end_time,
        'error_message': interface_log_dict['error_message'] if 'error_message' in interface_log_dict else '',
        's_header': interface_log_dict['s_header'] if 's_header' in interface_log_dict else '',
        's_payload': interface_log_dict['s_payload'] if 's_payload' in interface_log_dict else '',
        'r_code': interface_log_dict['r_code'] if 'r_code' in interface_log_dict else '',
        'r_header': interface_log_dict['r_header'] if 'r_header' in interface_log_dict else '',
        'r_payload': interface_log_dict['r_payload'] if 'r_payload' in interface_log_dict else ''
    })


@try_except
def use_case_exception_log_update(use_case_log_id, use_case_start):
    """
    用例执行过程中抛出异常时
    更新用例的运行日志
    :param use_case_log_id:
    :param use_case_start:
    :return:
    """
    use_case_stop = timeit.default_timer()
    end_time = datetime.utcnow()
    return RunLogAPI.modify_use_case_run_log(**{
        'id': use_case_log_id,
        'is_pass': False,
        'end_time': end_time,
        'cost_time': use_case_stop - use_case_start
    })


@app.context_processor
def run_use_case(use_case_id, batch_log_id=None, environment_id=None, relation_id=None,
                 use_case_count=None, batch_start_timer=None, async=False, auto_run=False, alarm_monitor=False):

    # if async:
    #     engine.dispose()
    exec_result_list = []
    interface_count = 1

    # 信息初始化
    start_time = datetime.utcnow()
    use_case_start = timeit.default_timer()
    run_pass = True
    use_case_log_info = {
        'use_case_id': use_case_id,
        'start_time': start_time,
        'auto_run': auto_run
    }
    if batch_log_id:
        use_case_log_info['batch_run_log_id'] = batch_log_id
    use_case_log_id = RunLogAPI.add_use_case_run_log(**use_case_log_info)

    # 获取用例信息以及用例下接口信息
    try:
        use_case_info = UseCaseAPI.get_use_case(id=use_case_id)[0]
        if relation_id:
            interface_list = UseCaseAPI.get_relation(id=relation_id)
        else:
            interface_list = UseCaseAPI.get_relation(use_case_id=use_case_id)
    except Exception as e:
        use_case_exception_log_update(use_case_log_id, use_case_start)
        return {'success': False,
                'error_str': '接口{0}数据库'.format(interface_count),
                'res': exec_result_list,
                'error': '{0}: {1}'.format(str(e.__class__.__name__), str(e)),
                'batch_log_id': batch_log_id,
                'use_case_count': use_case_count,
                'batch_start_timer': batch_start_timer
                }
    try:
        use_case_info['interface_list'] = []
        # 对用例中使用预定义参数的做参数替换
        for interface_relation in interface_list:
            eval_string = interface_relation['eval_string']
            interface_id = interface_relation['interface_id']
            interface_info = InterfaceAPI.get_interface(id=interface_id)[0]
            interface_info['interface_delay'] = interface_relation['interface_delay']
            interface_info['eval_string'] = eval_string

            interface_info['param_define_list'] = get_param_define_list(interface_relation['id'])
            use_case_info['interface_list'].append(interface_info)
        interface_list = use_case_info['interface_list']
    except Exception as e:
        # 用例运行日志记录
        use_case_exception_log_update(use_case_log_id, use_case_start)
        return {'success': False,
                'error_str': '接口{0}参数替换'.format(interface_count),
                'res': exec_result_list,
                'error': '{0}: {1}'.format(str(e.__class__.__name__), str(e)),
                'batch_log_id': batch_log_id,
                'use_case_count': use_case_count,
                'batch_start_timer': batch_start_timer
                }

    with requests.Session() as session:
        # 由于线上环境配置有host，所以监控模式下，也要配置环境信息
        # if not alarm_monitor:
        if not batch_log_id:
            environment_id = environment_id or use_case_info['environment_id']
        print(environment_id)
        environment_info = EnvironmentAPI.get_environment_line_info(environment_id=environment_id)
        for element in environment_info:
            url = element['url']
            ip_address = element['map_ip']
            g_DNS.add_new_dns(os.getpid(), {url: ip_address})

        for interface in interface_list:
            # 添加延时运行接口
            interface_delay = int(interface.get('interface_delay'))
            if interface_delay > 0:
                time.sleep(interface_delay)
            interface_name = interface.get('interface_name')
            interface_log_dict = {
                'interface_start_time': datetime.utcnow(),
                'use_case_run_log_id': use_case_log_id,
                'interface_id': interface['id']
            }
            try:
                # 将接口未替换的参数全部替换
                request_method = interface['interface_method']
                to_rephrase_list = [interface['interface_url'],
                                    interface['interface_header'],
                                    interface['interface_json_payload']]
                result_list = []
                param_define_list = interface['param_define_list']
                for item_to_rephrase in to_rephrase_list:
                    param_list = ParameterUtil.search_parameter(item_to_rephrase)
                    if param_list:
                        for item in param_list:
                            param_value = next((param for param in param_define_list
                                                if param["parameter_name"] == item))['parameter_value']
                            value_to_rephrase = ParameterUtil.search_parameter(param_value)
                            if value_to_rephrase:
                                for value_info in value_to_rephrase:
                                    order = int(value_info.split('|')[0])
                                    name = value_info.split('|')[1]
                                    if name == 'status_code':
                                        temp_string = 'exec_result_list[{0}]["status_code"]'.format(str(order - 1))
                                    elif name == 'header':
                                        temp_string = 'exec_result_list[{0}]["header"]'.format(str(order - 1))
                                    else:
                                        temp_string = 'exec_result_list[{0}]["json_response"]'.format(str(order - 1))
                                    param_value = param_value.replace('${{{0}}}'.format(value_info), temp_string)
                                a = []
                                exec_string = 'a.append({0})'.format(param_value)
                                exec(exec_string, locals(), locals())
                                new_param_value = '"{0}"'.format(a[0])
                                item_to_rephrase = item_to_rephrase.replace('${{{0}}}'.format(item), new_param_value)
                            else:
                                if item_to_rephrase == interface['interface_url']:
                                    item_to_rephrase = item_to_rephrase.replace('${{{0}}}'.format(item), '{0}'.
                                                                                format(param_value))
                                else:
                                    item_to_rephrase = item_to_rephrase.replace('${{{0}}}'.format(item), '"{0}"'.
                                                                                format(param_value))
                    result_list.append(item_to_rephrase)
                url = result_list[0]
                header = result_list[1]
                json_payload = result_list[2]
            except Exception as e:
                # 数据处理以及日志记录
                interface_log_dict['is_pass'] = False
                interface_log_dict['error_message'] = '参数替换: {0}: {1}'.format(str(e.__class__.__name__), str(e))
                interface_log_insert(interface_log_dict)
                # 用例运行日志记录
                use_case_exception_log_update(use_case_log_id, use_case_start)
                return {'success': False,
                        'error_str': '接口{0}参数替换'.format(interface_count),
                        'res': exec_result_list,
                        'error': '{0}: {1}'.format(str(e.__class__.__name__), str(e)),
                        'batch_log_id': batch_log_id,
                        'use_case_count': use_case_count,
                        'batch_start_timer': batch_start_timer
                        }

            try:
                # 加密
                if json_payload:
                    json_payload = json.loads(json_payload)
                    if interface['interface_encryption'] != 0:
                        encryption_method = EncryptionAPI.get_encryption_method(interface['interface_encryption'])
                        method = getattr(Encryption, encryption_method)
                        json_payload = method(json_payload)
            except Exception as e:
                # 数据处理以及日志记录
                interface_log_dict['is_pass'] = False
                interface_log_dict['error_message'] = 'json处理或加密: {0}: {1}'.format(str(e.__class__.__name__), str(e))
                interface_log_insert(interface_log_dict)
                # 用例运行日志记录
                use_case_exception_log_update(use_case_log_id, use_case_start)
                return {'success': False,
                        'error_str': '接口{0} json处理或加密'.format(interface_count),
                        'res': exec_result_list,
                        'error': '{0}: {1}'.format(str(e.__class__.__name__), str(e)),
                        'batch_log_id': batch_log_id,
                        'use_case_count': use_case_count,
                        'batch_start_timer': batch_start_timer
                        }

            # 请求接口参数准备
            request_kwargs = {
                'timeout': 10
            }
            if header:
                request_kwargs['headers'] = json.loads(header)
            if json_payload:
                if interface['body_type'] == 0:
                    request_kwargs['json'] = json_payload
                else:
                    request_kwargs['data'] = json_payload

            # 获取域名对应的服务名
            get_server_name_dict = {
                "_head": {
                    "_version": "0.01",
                    "_msgType": "request",
                    "_timestamps": "",
                    "_invokeId": "",
                    "_callerServiceId": "",
                    "_groupNo": "",
                    "_interface": "get_server_name",
                    "_remark": ""
                },
                "_params": {
                    "strUrl": url
                }
            }
            try:
                response = requests.post('http://123.207.51.243:8000/base_server', json=get_server_name_dict, timeout=5)
                server_name = response.json()['_data']['retInfo']['serverName']
            except Exception as e:
                server_name = '获取服务名失败:'.format(str(e))

            # 获取方法ID, 接口名
            requested_interface = ''
            if json_payload:
                if 'head' in json_payload:
                    if 'interface' in json_payload['head']:
                        requested_interface = json_payload['head']['interface']
                elif '_head' in json_payload:
                    if '_interface' in json_payload['_head']:
                        requested_interface = json_payload['_head']['_interface']
            if not requested_interface:
                try:
                    requested_interface = url.split('//')[1].split('/')[0]
                except:
                    requested_interface = interface['interface_url'].split('//')[1].split('/')[0]

            # 日志内容
            interface_log_dict['s_header'] = header if header else ''
            interface_log_dict['s_payload'] = json.dumps(json_payload, ensure_ascii=False) if json_payload else ''
            interface_log_dict['interface_start'] = timeit.default_timer()

            request_exception = False
            log_report_code = 0
            error_string = ''
            json_response = dict()
            result = dict()
            request_method = request_method.upper()
            try:
                r = session.request(request_method, url, **request_kwargs)
                r.encoding = 'utf-8'
                try:
                    json_response = r.json()
                    json_flag = True
                except Exception as e:
                    print(str(e))
                    json_flag = False
                    r_type = r.headers['Content-Type']
                    if 'application/json' != r_type:
                        json_response = r.text
                    else:
                        json_response = {}
                interface_log_dict['interface_stop'] = timeit.default_timer()
                result = {
                    'status_code': r.status_code,
                    'header': dict(r.headers),
                    'json_response': json_response,
                    'interface_name': interface_name
                }
                interface_log_dict['r_code'] = r.status_code
                interface_log_dict['r_header'] = json.dumps(result['header'], ensure_ascii=False)
                if json_flag:
                    interface_log_dict['r_payload'] = json.dumps(result['json_response'], ensure_ascii=False)
                else:
                    r.encoding = 'utf-8'
                    interface_log_dict['r_payload'] = r.text
                    result['json_response'] = '<iframe srcdoc="{}" style="width:100%;height:60vh" ' \
                                              'frameborder="0"></iframe>'.format(html.escape(r.text))
            except ConnectTimeout as e:
                request_exception = True
                error_string = '{0}: {1} ，{2}'.format('请求服务连接超时', str(e.__class__.__name__), str(e))
                log_report_code = '9991'
            except ConnectionError as e:
                if os.getpid() in g_DNS.get_dns():
                    dns_info = g_DNS.get_dns()[os.getpid()]
                    LOGGER.info_log('连接失败，环境映射信息：{}'.format(dns_info))
                request_exception = True
                error_string = '{0}，{1}: {2}'.format('请求服务连接失败', str(e.__class__.__name__), str(e))
                log_report_code = '9992'
            except KeyError as e:
                request_exception = True
                error_string = '错误代码行{0}: {1}'.format(sys._getframe().f_lineno, str(e))
                log_report_code = '99924'
            except Exception as e:
                request_exception = True
                error_string = '{0}: {1}，{2}'.format(sys._getframe().f_lineno, str(e.__class__.__name__), str(e))
                log_report_code = '9993'
            finally:
                if request_exception:
                    if alarm_monitor:
                        if not app.config['DEBUG']:
                            cost_time = timeit.default_timer() - interface_log_dict['interface_start']
                            LOGGER.request_log(server_name, server_name, requested_interface, log_report_code, str(cost_time))

                    # 数据处理以及日志记录
                    interface_log_dict['is_pass'] = False
                    interface_log_dict['error_message'] = '{0}'.format(error_string)
                    interface_log_insert(interface_log_dict)
                    # 用例运行日志记录
                    use_case_exception_log_update(use_case_log_id, use_case_start)
                    return {'success': False,
                            'error_str': '接口{0}请求'.format(interface_count),
                            'res': exec_result_list,
                            'error': error_string,
                            'batch_log_id': batch_log_id,
                            'use_case_count': use_case_count,
                            'batch_start_timer': batch_start_timer
                            }

            try:
                # 验证接口返回
                eval_string = interface['eval_string']
                if eval_string:
                    eval_string = eval_string.replace('${status_code}', 'result["status_code"]') \
                        .replace('${header}', 'result["header"]') \
                        .replace('${json_payload}', 'result["json_response"]')
                    a = []
                    exec_string = 'a.append({0})'.format(eval_string)
                    exec(exec_string)
                    eval_success = a[0]
                else:
                    eval_success = True
                result['success'] = eval_success
                run_pass = run_pass and eval_success
                exec_result_list.append(result)
                # 数据处理以及日志记录
                interface_log_dict['is_pass'] = result['success']
                interface_log_insert(interface_log_dict)

                if alarm_monitor:
                    if not app.config['DEBUG']:
                        cost_time = interface_log_dict['interface_stop'] - interface_log_dict['interface_start']
                        ret_code = '' if eval_success else '1'
                        if not ret_code:
                            if 'body' in json_response:
                                if 'ret' in json_response['body']:
                                    ret_code = json_response['body']['ret']
                            elif '_data' in json_response:
                                if '_ret' in json_response['_data']:
                                    ret_code = json_response['_data']['_ret']
                            else:
                                ret_code = '0'
                        LOGGER.request_log(server_name, server_name, requested_interface, ret_code, str(cost_time))

                if not result['success']:
                    run_pass = False
                    break
            except Exception as e:
                # if auto_run:
                #     if not app.config['DEBUG']:
                #         error_str = '接口名称:{}, 参数验证出错，{0}: {1}'.format(str(e.__class__.__name__), str(e))
                        # LOGGER.exception_log(error_str)

                result['success'] = False
                exec_result_list.append(result)
                # 数据处理以及日志记录
                interface_log_dict['is_pass'] = result['success']
                exc_type, exc_obj, exc_tb = sys.exc_info()
                interface_log_dict['error_message'] = '验证: {0}: {1},异常信息：{2}'.format(str(e.__class__.__name__), str(e), str(traceback.extract_tb(exc_tb)))
                interface_log_insert(interface_log_dict)
                # 用例运行日志记录
                use_case_exception_log_update(use_case_log_id, use_case_start)
                return {'success': False,
                        'error_str': '接口{0}验证'.format(interface_count),
                        'res': exec_result_list,
                        'error': '{0}: {1}'.format(str(e.__class__.__name__), str(e)),
                        'batch_log_id': batch_log_id,
                        'use_case_count': use_case_count,
                        'batch_start_timer': batch_start_timer
                        }

            interface_count += 1

    # 用例运行日志记录
    use_case_stop = timeit.default_timer()
    end_time = datetime.utcnow()
    RunLogAPI.modify_use_case_run_log(**{
        'id': use_case_log_id,
        'is_pass': run_pass,
        'end_time': end_time,
        'cost_time': use_case_stop - use_case_start
    })

    return {'pass': run_pass,
            'res': exec_result_list,
            'batch_log_id': batch_log_id,
            'use_case_count': use_case_count,
            'batch_start_timer': batch_start_timer}


@try_except
def run_use_case_callback(obj):
    result = obj.result()
    batch_log_id = result['batch_log_id']
    batch_log = RunLogAPI.get_batch_run_log_info(id=batch_log_id)
    if not batch_log:
        return
    if batch_log[0]['pass_rate'] != -1:
        return
    use_case_count = result['use_case_count']
    use_case_run_logs = RunLogAPI.get_use_case_run_log(batch_run_log_id=batch_log_id)
    finished_use_case = 0
    for use_case_log in use_case_run_logs:
        if use_case_log['cost_time'] != 0.0:
            finished_use_case += 1
    if finished_use_case == use_case_count:
        batch_start_timer = result['batch_start_timer']
        batch_end_timer = timeit.default_timer()
        success_count = 0
        for run_log in use_case_run_logs:
            if run_log['is_pass']:
                success_count += 1
        pass_rate = int(success_count / use_case_count * 100)
        RunLogAPI.modify_batch_run_log(**{
            'id': batch_log_id,
            'pass_rate': pass_rate,
            'end_time': datetime.utcnow(),
            'cost_time': batch_end_timer - batch_start_timer
        })


@try_except
def run_use_case_async(use_case_id, batch_log_id=None, environment_id=None, use_case_count=None,
                       batch_start_timer=None, auto_run=False, alarm_monitor=False):
    if batch_log_id:
        executor.submit(run_use_case, use_case_id, batch_log_id, environment_id, None, use_case_count,
                        batch_start_timer, True, auto_run, alarm_monitor).\
            add_done_callback(run_use_case_callback)
    else:
        executor.submit(run_use_case, use_case_id, batch_log_id, environment_id, None, use_case_count,
                        batch_start_timer, True, auto_run, alarm_monitor)


@try_except
def run_batch(batch_id, environment_id=0, auto_run=False, alarm_monitor=False):
    start_timer = timeit.default_timer()
    relation_list = BatchAPI.get_batch_use_case_relation(batch_id=batch_id)
    use_case_count = len(relation_list)
    start_time = datetime.utcnow()
    batch_log_id = RunLogAPI.add_batch_run_log(**{
        'batch_id': batch_id,
        'use_case_count': use_case_count,
        'start_time': start_time
    })

    counter = 0
    for relation in relation_list:
        counter += 1
        use_case = UseCaseAPI.get_use_case(id=relation['use_case_id'])[0]
        run_use_case_async(use_case['id'], batch_log_id, environment_id=environment_id, use_case_count=use_case_count,
                           batch_start_timer=start_timer, auto_run=auto_run, alarm_monitor=alarm_monitor)


def get_param_define_list(relation_id=None):
    param_define_list = UseCaseAPI.get_case_parameter_relation(relation_id=relation_id)
    param_list = []
    for param in param_define_list:
        pattern = re.compile(r'\${param\|[^${}]*}|^random\(.*\)|\${timestamps}')
        match_result = pattern.findall(param['parameter_value'])
        if match_result:
            if 'random' in match_result[0]:
                param_value = ParameterUtil.random_length_seq(match_result[0])
            elif '${timestamps}' in match_result:
                param_value = str(int(time.time()))
            else:
                param_name = match_result[0].split('|')[1].replace('}', '')
                param_value = ParameterAPI.get_parameter(parameter_name=param_name)[0]['value']
            param['parameter_value'] = param_value
        param_list.append(param)
    return param_list

