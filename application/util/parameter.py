import re


def search_parameter(input_string):
    """
    在给定字符串中查找被 ${} 包裹的所有参数, 并以列表返回
    :param input_string:        给定用来搜索参数的字符串
    :return:                    参数列表
    """
    pattern = re.compile(r'\${[^${}]*}')
    match_result = pattern.findall(input_string)
    param_list = []
    for item in match_result:
        param_list.append(item.replace('${', '').replace('}', ''))
    return param_list
