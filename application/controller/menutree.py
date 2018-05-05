# -*- coding: utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import menutree as MenuTreeAPI


@app.route('/menu_tree/system_line/info', methods=['POST'])
def get_system_line():
    """
    查询所有系统菜单
    :return:
    """
    try:
        result = MenuTreeAPI.query_system_line(**jsonify())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/menu_tree/business_line/info', methods=['POST'])
def get_business_line():
    """
    查询所有业务菜单
    :return:
    """
    try:
        result = MenuTreeAPI.query_business_line(**jsonify())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/menu_tree/function_line/info', methods=['POST'])
def get_function_line():
    """
    查询所有功能模块菜单
    :return:
    """
    try:
        result = MenuTreeAPI.query_function_line(**jsonify())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    return jsonify({'success': True, 'res': result})


@app.route('/menu_tree/info', methods=['POST'])
def get_menu_tree():
    """
    查询所有菜单
    :return:
    """
    try:
        re_system = MenuTreeAPI.query_system_line(**request.get_json())
        re_business = MenuTreeAPI.query_business_line(**request.get_json())
        re_function = MenuTreeAPI.query_function_line(**request.get_json())
    except Exception as e:
        return jsonify({'success': False, 'res': str(e)})
    menu_tree = []
    for business_line in re_business:
        business_line_id = business_line.pop('id')
        business_line['business_name'] = business_line.pop('business_name')
        business_line['system_line'] = []
        for sys_line in re_system:
            if not business_line_id == sys_line.get('business_line_id'):
                continue
            sys_line.pop('business_line_id')
            system_line_id = sys_line.pop('id')
            sys_line['function_line'] = []
            for function_line in re_function:
                if not system_line_id == function_line.get('system_line_id'):
                    continue
                function_line.pop('id')
                function_line.pop('system_line_id')
                sys_line['function_line'].append(function_line)
            business_line['system_line'].append(sys_line)
        menu_tree.append({'business_line': business_line})
    return jsonify({'success': True, 'res': menu_tree})
