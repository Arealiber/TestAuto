from sqlalchemy import desc

from application import session_scope
from application.model.script import Script, ScriptInterfaceRelation


def add_script(**kwargs):
    with session_scope() as session:
        script = Script(**kwargs)
        session.add(script)


def get_script(**kwargs):
    with session_scope() as session:
        script_list = session.query(Script).filter_by(**kwargs).filter_by(status=1)
        session.expunge_all()
    return script_list


def modify_script(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Script).filter_by(id=id).update(kwargs)


def del_script(**kwargs):
    """
    删除script
    同时将所有该script的关联关系清除
    :param kwargs:
    :return:
    """
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Script).filter_by(id=id).update({'status': 0})
        session.query(ScriptInterfaceRelation).filter_by(script_id=id).update({'status': 0})


def get_max_order(script_id):
    """
    获取某script下interface的最大order数
    :param script_id:           script id
    :return:                    最大order数
    """
    with session_scope() as session:
        max_order_relation = session\
            .query(ScriptInterfaceRelation)\
            .filter_by(script_id=script_id, status=1)\
            .order_by(desc(ScriptInterfaceRelation.order))\
            .first()
        if not max_order_relation:
            return 0
        else:
            return max_order_relation.order


def add_relation(script_id, interface_id, order=None):
    """
    将某interface与script关联
    如未传入order则加入到最后
    如传入order则大于当前order的全部加一
    :param script_id:           script id
    :param interface_id:        interface id
    :param order:               interface顺序，如果为空加入到最后
    :return:
    """
    with session_scope() as session:
        if not order:
            order = get_max_order(script_id) + 1
        else:
            session\
                .query(ScriptInterfaceRelation)\
                .filter_by(script_id=script_id)\
                .filter(ScriptInterfaceRelation.order >= order)\
                .update({'order': ScriptInterfaceRelation.order + 1})
        relation = ScriptInterfaceRelation(script_id=script_id, interface_id=interface_id, order=order)
        session.add(relation)


def get_relation(script_id):
    with session_scope() as session:
        relation_list = session\
            .query(ScriptInterfaceRelation)\
            .filter_by(script_id=script_id)\
            .filter_by(status=1)
        session.expunge_all()
    return relation_list


def del_relation(relation_id):
    """
    删除script与interface关系
    如果有order大于当前删除order的，全部减一
    :param relation_id:           relation id
    :return:
    """
    with session_scope() as session:
        relation = session.query(ScriptInterfaceRelation).filter_by(id=relation_id).one()
        current_order = relation.order
        script_id = relation.script_id
        session.query(ScriptInterfaceRelation).filter_by(id=relation_id).update({'status': 0})
        session\
            .query(ScriptInterfaceRelation)\
            .filter_by(script_id=script_id)\
            .filter(ScriptInterfaceRelation.order > current_order)\
            .update({'order': ScriptInterfaceRelation.order - 1})


def reorder_relation(relation_id, new_order):
    """
    调整某个已有interface的order
    同时将其他影响范围内的interface的order全部加一或者减一
    :return:
    """
    with session_scope() as session:
        relation = session.query(ScriptInterfaceRelation).filter_by(id=relation_id).one()
        current_order = relation.order
        script_id = relation.script_id
        if current_order == new_order:
            return
        elif current_order < new_order:
            session\
                .query(ScriptInterfaceRelation)\
                .filter_by(script_id=script_id)\
                .filter(ScriptInterfaceRelation.order > current_order)\
                .filter(ScriptInterfaceRelation.order <= new_order)\
                .update({'order': ScriptInterfaceRelation.order - 1})
        elif current_order > new_order:
            session\
                .query(ScriptInterfaceRelation)\
                .filter_by(script_id=script_id)\
                .filter(ScriptInterfaceRelation.order < current_order )\
                .filter(ScriptInterfaceRelation.order >= new_order)\
                .update({'order': ScriptInterfaceRelation.order + 1})
        session\
            .query(ScriptInterfaceRelation)\
            .filter_by(id=relation_id)\
            .update({'order': new_order})
