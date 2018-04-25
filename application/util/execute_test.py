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

executor = ProcessPoolExecutor()


def run_use_case(use_case_id, batch_log_id=None, use_case_count=None, batch_start_timer=None):
    # 获取用例信息以及用例下接口信息
    try:
        use_case_info = Case_API.get_use_case(id=use_case_id)[0]
        interface_list = Case_API.get_relation(use_case_id=use_case_id)

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

        # 信息初始化
        start_time = datetime.utcnow()
        use_case_start = timeit.default_timer()
        run_pass = True
        use_case_id = use_case_info['id']
        if batch_log_id:
            use_case_log_id = RunLogAPI.add_use_case_run_log(**{
                'use_case_id': use_case_id,
                'start_time': start_time,
                'batch_run_log_id': batch_log_id
            })
        else:
            use_case_log_id = RunLogAPI.add_use_case_run_log(**{
                'use_case_id': use_case_id,
                'start_time': start_time,
            })
        interface_list = use_case_info['interface_list']
        session = requests.Session()
        exec_result_list = []

        # 将接口未替换的参数全部替换
        for interface in interface_list:
            interface_start_time = datetime.utcnow()
            interface_start = timeit.default_timer()

            request_method = interface['interface_method']
            to_rephrase_list = [interface['interface_url'], interface['interface_header'], interface['interface_json_payload']]
            result_list = []
            param_define_list = interface['param_define_list']
            for item_to_rephrase in to_rephrase_list:
                param_list = ParameterUtil.search_parameter(item_to_rephrase)
                if param_list:
                    for item in param_list:
                        param_value = next((param for param in param_define_list if param["parameter_name"] == item))['parameter_value']
                        value_to_rephrase = ParameterUtil.search_parameter(param_value)
                        if value_to_rephrase:
                            value_info = ParameterUtil.search_parameter(param_value)[0]
                            order = int(value_info.split('|')[0])
                            name = value_info.split('|')[1]
                            result_dict = exec_result_list[order - 1]
                            if name == 'status_code':
                                temp_dict = result_dict['status_code']
                            elif name == 'header':
                                temp_dict = result_dict['header']
                            else:
                                temp_dict = result_dict['json_response']
                            to_exec = param_value.replace('${{{0}}}'.format(value_info), 'temp_dict')
                            a = []
                            exec_string = 'a.append({0})'.format(to_exec)
                            exec(exec_string)
                            new_param_value = '"{0}"'.format(a[0])
                            item_to_rephrase = item_to_rephrase.replace('${{{0}}}'.format(item), new_param_value)
                        else:
                            item_to_rephrase = item_to_rephrase.replace('${{{0}}}'.format(item), '"{0}"'.format(param_value))
                result_list.append(item_to_rephrase)
            url = result_list[0]
            header = result_list[1]
            json_payload = result_list[2]

            # 加密
            if json_payload:
                json_payload = json.loads(json_payload)
                json_payload = Encryption.huan_ji_xia_encryption(json_payload)

            # 请求接口
            if request_method.upper() == 'GET':
                if header:
                    r = session.get(url, headers=header, json=json_payload, timeout=10)
                else:
                    r = session.get(url, json=json_payload, timeout=10)
            elif request_method.upper() == 'POST':
                if header:
                    r = session.post(url, headers=header, json=json_payload, timeout=10)
                else:
                    r = session.post(url, json=json_payload, timeout=10)
            result = {
                'status_code': r.status_code,
                'header': json.dumps(dict(r.headers)),
                'json_response': r.json()
            }

            # 验证接口返回
            eval_string = interface['eval_string']
            if eval_string:
                eval_string = eval_string.replace('${status_code}', 'result["status_code"]')\
                    .replace('${header}', 'result["header"]')\
                    .replace('${json_payload}', 'result["json_response"]')
                a = []
                exec_string = 'a.append({0})'.format(eval_string)
                print(exec_string)
                exec(exec_string)

                eval_success = a[0]
            else:
                eval_success = True
            result['success'] = eval_success
            run_pass = run_pass and eval_success
            exec_result_list.append(result)

            # 数据处理以及日志记录
            interface_end_time = datetime.utcnow()
            interface_stop = timeit.default_timer()
            RunLogAPI.add_interface_run_log(**{
                'use_case_run_log_id': use_case_log_id,
                'interface_id': interface['id'],
                'r_code': result['status_code'],
                'r_header': json.dumps(result['header']),
                'r_payload': json.dumps(result['json_response']),
                'is_pass': result['success'],
                'cost_time': interface_stop - interface_start,
                'start_time': interface_start_time,
                'end_time': interface_end_time
            })

        use_case_stop = timeit.default_timer()
        end_time = datetime.utcnow()

        # 日志记录
        RunLogAPI.modify_use_case_run_log(**{
            'id': use_case_log_id,
            'is_pass': run_pass,
            'end_time': end_time,
            'cost_time': use_case_stop - use_case_start
        })

    except Exception as e:
        return {'success': False, 'error': '{0}: {1}'.format(str(e.__class__.__name__), str(e))}

    return {'pass': run_pass,
            'res': exec_result_list,
            'batch_log_id': batch_log_id,
            'use_case_count': use_case_count,
            'batch_start_timer': batch_start_timer}


def run_use_case_callback(obj):
    result = obj.result()
    batch_log_id = result['batch_log_id']
    batch_log = RunLogAPI.get_multi_batch_run_log_info(id=batch_log_id)[0]
    if batch_log['pass_rate'] != -1:
        return
    use_case_count = result['use_case_count']
    use_case_run_logs = RunLogAPI.get_use_case_run_log(batch_run_log_id=batch_log_id)
    finished_use_case = len(use_case_run_logs)
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
    executor.submit(run_use_case, use_case_id, batch_log_id, use_case_count, batch_start_timer).add_done_callback(run_use_case_callback)


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
