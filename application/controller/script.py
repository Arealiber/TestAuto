from flask import request, jsonify

from application import app
from application.api import interface as InterfaceAPI
from application.api import script as ScriptAPI


@app.route('/script/add', methods=['POSt'])
def add_script():
    pass


@app.route('/script/list', methods=['POST'])
def script_list():
    """
    获取script列表，不需要获取script包含的interface
    :return:
    """
    pass


@app.route('/script/detail', methods=['POST'])
def script_detail():
    """
    获取某个script的详细信息，包括其包含的interface列表
    :return:
    """
    pass


@app.route('/script/update', methods=['POST'])
def update_script():
    """
    更新script内容，不更新与interface的关联
    :return:
    """
    pass


@app.route('/script/delete', methods=['POST'])
def del_script():
    """
    删除script
    :return:
    """
    pass


@app.route('/script/relation/add', methods=['POST'])
def add_relation():
    """
    将某个interface与某个script关联
    :return:
    """
    pass


@app.route('/script/relation/delete', methods=['POST'])
def del_relation():
    """
    解除某个interface与script的关联
    :return:
    """
    pass


@app.route('/script/relation/reorder', methods=['POST'])
def reorder_relation():
    """
    重新排序某个interface在script中的顺序
    :return:
    """
    pass
