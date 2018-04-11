# -*- coding:utf-8 -*-
from flask import request, jsonify

from application import app
from application.api import interface as InterfaceAPI
from application.api import use_case as API


"""
用例

"""


@app.route('/use_case/add', methods=['POST'])
def add_use_case():
    """
    添加use_case，只包含用例基础信息
    """
    pass


@app.route('/use_case/list', methods=['POST'])
def use_case_list():
    """
    获取use_case列表，不需要获取与use_case关联的interface
    """
    pass


@app.route('/use_case/detail', methods=['POST'])
def use_case_detail():
    """
    获取某个use_case的详细信息，包括其包含的interface列表
    1. 根据use_case id获取use_case基本信息
    2. 根据use_case_id获取use_case与interface的关联信息
    3. 根据关联信息的id查出所有interface的名称信息以及定义的参数信息
    4. 信息整理并返回
    """
    pass


@app.route('/use_case/update', methods=['POST'])
def update_use_case():
    """
    更新use_case内容，不更新与interface的关联
    """
    pass


@app.route('/use_case/delete', methods=['POST'])
def del_use_case():
    """
    删除use_case
    """
    pass


@app.route('/use_case/execute', methods=['POST'])
def execute_use_case():
    """
    手动执行某个use_case
    先不写，等测试流程实现再补上
    """
    pass


@app.route('/use_case/relation/add', methods=['POST'])
def add_relation():
    """
    将某个interface与某个use_case关联
    1. 关联use_case与interface
    2. 查找interface内parameter信息, 用空值为每个参数在relation下生成记录
    """
    pass


@app.route('/use_case/relation/delete', methods=['POST'])
def del_relation():
    """
    解除某个interface与use_case的关联
    """
    pass


@app.route('/use_case/relation/reorder', methods=['POST'])
def reorder_relation():
    """
    重新排序某个interface在use_case中的顺序
    """
    pass


@app.route('/use_case/relation/parameter/modify', methods=['POST'])
def relation_update_parameter():
    """
    更新某个
    """
    pass
