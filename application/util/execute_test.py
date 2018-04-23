import requests
import json

from application.util import encryption as Encryption
from application.util import parameter as ParameterUtil


def run_use_case(use_case_info):
    run_pass = True
    use_case_id = use_case_info['id']
    interface_list = use_case_info['interface_list']
    session = requests.Session()
    exec_result_list = []

    for interface in interface_list:
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
                        item_to_rephrase = item_to_rephrase.replace('${{{0}}}'.format(item), param_value)
            result_list.append(item_to_rephrase)
        url = result_list[0]
        header = result_list[1]
        json_payload = result_list[2]

        if json_payload:
            json_payload = json.loads(json_payload)
            json_payload = Encryption.huan_ji_xia_encryption(json_payload)

        if request_method.upper() == 'GET':
            if header:
                r = session.get(url, headers=header, json=json_payload)
            else:
                r = session.get(url, json=json_payload)
        elif request_method.upper() == 'POST':
            if header:
                r = session.post(url, headers=header, json=json_payload)
            else:
                r = session.post(url, json=json_payload)
        result = {
            'status_code': r.status_code,
            'header': json.dumps(dict(r.headers)),
            'json_response': r.json()
        }

        eval_string = interface['eval_string']
        eval_string = eval_string.replace('${status_code}', 'result["status_code"]')\
            .replace('${header}', 'result["header"]')\
            .replace('${json_payload}', 'result["json_response"]')
        a = []
        exec_string = 'a.append({0})'.format(eval_string)
        exec(exec_string)

        eval_success = a[0]
        result['success'] = eval_success
        run_pass = run_pass and eval_success
        exec_result_list.append(result)

    return {'pass': run_pass, 'res': exec_result_list}
