import re
import random


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


def random_length_seq(input_string):
    """

    :param input_string:
    :return:
    """
    digits = '0123456789'
    str_letters = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    pattern = re.compile(r'\d+')
    match_result = pattern.findall(input_string)
    if 'str' in input_string and match_result:
        return ''.join([random.choice(digits + str_letters) for _ in range(int(match_result[0]))])
    elif match_result:
        return ''.join([random.choice(digits) for _ in range(int(match_result[0]))])
    else:
        return None

