import requests
import json
import timeit
import re
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

from application.util import encryption as Encryption
from application.util import parameter as ParameterUtil
from application.api import run_log as RunLogAPI
from application.api import interface as InterfaceAPI
from application.api import use_case as Case_API
from application.api import parameter as ParameterAPI
from application.api import batch as BatchAPI
from application.api import use_case as UseCaseAPI
from application.api import encryption as EncryptionAPI
from application import engine

executor = ProcessPoolExecutor()


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


def run_use_case(use_case_id, batch_log_id=None, use_case_count=None, batch_start_timer=None, async=False):
    if async:
        engine.dispose()
    exec_result_list = []
    interface_count = 1
    # 获取用例信息以及用例下接口信息
    try:
        use_case_info = Case_API.get_use_case(id=use_case_id)[0]
        interface_list = Case_API.get_relation(use_case_id=use_case_id)
    except Exception as e:
        return {'success': False,
                'error_str': '接口{0}数据库'.format(interface_count),
                'res': exec_result_list,
                'error': '{0}: {1}'.format(str(e.__class__.__name__), str(e)),
                'batch_log_id': batch_log_id,
                'use_case_count': use_case_count,
                'batch_start_timer': batch_start_timer
                }

    # 信息初始化
    start_time = datetime.utcnow()
    use_case_start = timeit.default_timer()
    run_pass = True
    use_case_id = use_case_info['id']
    use_case_log_info = {
        'use_case_id': use_case_id,
        'start_time': start_time
    }
    if batch_log_id:
        use_case_log_info['batch_run_log_id'] = batch_log_id
    use_case_log_id = RunLogAPI.add_use_case_run_log(**use_case_log_info)

    try:
        use_case_info['interface_list'] = []
        # 对用例中使用预定义参数的做参数替换
        for interface_relation in interface_list:
            eval_string = interface_relation['eval_string']
            interface_id = interface_relation['interface_id']
            interface_info = InterfaceAPI.get_interface(id=interface_id)[0]
            interface_info['eval_string'] = eval_string

            interface_info['param_define_list'] = []
            param_define_list = Case_API.get_case_parameter_relation(relation_id=interface_relation['id'])
            for param in param_define_list:
                pattern = re.compile(r'\${param\|[^${}]*}')
                match_result = pattern.findall(param['parameter_value'])
                if match_result:
                    param_name = match_result[0].split('|')[1].replace('}', '')
                    param_value = ParameterAPI.get_parameter(parameter_name=param_name)[0]['value']
                    param['parameter_value'] = param_value
                interface_info['param_define_list'].append(param)

            use_case_info['interface_list'].append(interface_info)

        interface_list = use_case_info['interface_list']
        session = requests.Session()
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

        # 将接口未替换的参数全部替换
    for interface in interface_list:
        interface_log_dict = {
            'interface_start_time': datetime.utcnow(),
            'use_case_run_log_id': use_case_log_id,
            'interface_id': interface['id']
        }
        try:
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
                        param_value = next((param for param in param_define_list if param["parameter_name"] == item))['parameter_value']
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
                            item_to_rephrase = item_to_rephrase.replace('${{{0}}}'.format(item), '"{0}"'.format(param_value))
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

        # 请求接口
        request_kwargs = {
            'timeout': 10
        }
        interface_log_dict['s_header'] = header if header else ''
        interface_log_dict['s_payload'] = json.dumps(json_payload, ensure_ascii=False) if json_payload else ''
        if header:
            request_kwargs['headers'] = json.loads(header)
        if json_payload:
            if interface['body_type'] == 0:
                request_kwargs['json'] = json_payload
            else:
                request_kwargs['data'] = json_payload
        interface_log_dict['interface_start'] = timeit.default_timer()
        try:
            if request_method.upper() == 'GET':
                r = session.get(url, **request_kwargs)
            elif request_method.upper() == 'POST':
                r = session.post(url, **request_kwargs)
            try:
                json_response = r.json()
            except Exception as e:
                json_response = {}
            interface_log_dict['interface_stop'] = timeit.default_timer()
            result = {
                'status_code': r.status_code,
                'header': dict(r.headers),
                'json_response': json_response
            }
            interface_log_dict['r_code'] = r.status_code
            interface_log_dict['r_header'] = json.dumps(result['header'], ensure_ascii=False)
            interface_log_dict['r_payload'] = json.dumps(result['json_response'], ensure_ascii=False)
        except Exception as e:
            # 数据处理以及日志记录
            interface_log_dict['is_pass'] = False
            interface_log_dict['error_message'] = '请求: {0}: {1}'.format(str(e.__class__.__name__), str(e))
            interface_log_insert(interface_log_dict)
            # 用例运行日志记录
            use_case_exception_log_update(use_case_log_id, use_case_start)
            return {'success': False,
                    'error_str': '接口{0}请求'.format(interface_count),
                    'res': exec_result_list,
                    'error': '{0}: {1}'.format(str(e.__class__.__name__), str(e)),
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

            if not result['success']:
                run_pass = False
                break
        except Exception as e:
            result['success'] = False
            exec_result_list.append(result)
            # 数据处理以及日志记录
            interface_log_dict['is_pass'] = result['success']
            interface_log_dict['error_message'] = '验证: {0}: {1}'.format(str(e.__class__.__name__), str(e))
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


def run_use_case_callback(obj):
    result = obj.result()
    batch_log_id = result['batch_log_id']
    batch_log = RunLogAPI.get_batch_run_log_info(id=batch_log_id)[0]
    if batch_log['pass_rate'] != -1:
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
    else:
        return


def run_use_case_async(use_case_id, batch_log_id=None, use_case_count=None, batch_start_timer=None):
    if batch_log_id:
        executor.submit(run_use_case, use_case_id, batch_log_id, use_case_count, batch_start_timer, True).\
            add_done_callback(run_use_case_callback)
    else:
        executor.submit(run_use_case, use_case_id, batch_log_id, use_case_count, batch_start_timer, True)


def run_batch(batch_id):
    start_timer = timeit.default_timer()
    relation_list = BatchAPI.get_batch_use_case_relation(batch_id=batch_id)
    use_case_count = len(relation_list)
    start_time = datetime.utcnow()
    batch_log_id = RunLogAPI.add_batch_run_log(**{
        'batch_id': batch_id,
        'use_case_count': use_case_count,
        'start_time': start_time
    })

    for relation in relation_list:
        use_case = UseCaseAPI.get_use_case(id=relation['use_case_id'])[0]
        run_use_case_async(use_case['id'], batch_log_id, use_case_count, start_timer)
