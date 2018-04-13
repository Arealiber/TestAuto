# -*- coding: utf-8 -*-
from sqlalchemy import desc
from application import session_scope
from application.model.use_case import UseCase, UseCaseInterfaceRelation, UseCaseParameterRelation


def add_use_case(**kwargs):
    with session_scope() as session:
        script = UseCase(**kwargs)
        session.add(script)


def get_use_case(**kwargs):
    with session_scope() as session:
        query = session.query(UseCase).filter_by(**kwargs).filter_by(status=1)
    use_case_list = [use_case.to_dict() for use_case in query]
    return use_case_list


def modify_use_case(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(UseCase).filter_by(id=id).update(kwargs)


def del_use_case(**kwargs):
    """
    删除use_case
    同时将所有该use_case的关联关系清除
    :param kwargs:
    :return:
    """
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(UseCase).filter_by(id=id).update({'status': 0})
        session.query(UseCaseInterfaceRelation).filter_by(use_case_id=id).update({'status': 0})


def get_max_order(use_case_id):
    """
    获取某use_case下interface的最大order数
    :param use_case_id:         use_case id
    :return:                    最大order数
    """
    with session_scope() as session:
        max_order_relation = session\
            .query(UseCaseInterfaceRelation)\
            .filter_by(use_case_id=use_case_id, status=1)\
            .order_by(desc(UseCaseInterfaceRelation.order))\
            .first()
        if not max_order_relation:
            return 0
        else:
            return max_order_relation.order


def add_relation(use_case_id, interface_id, order=None):
    """
    将某interface与use_case关联
    如未传入order则加入到最后
    如传入order则大于当前order的全部加一
    :param use_case_id:         use_case id
    :param interface_id:        interface id
    :param order:               interface顺序，如果为空加入到最后
    :return:
    """
    with session_scope() as session:
        if not order:
            order = get_max_order(use_case_id) + 1
        else:
            session\
                .query(UseCaseInterfaceRelation)\
                .filter_by(use_case_id=use_case_id)\
                .filter(UseCaseInterfaceRelation.order >= order)\
                .update({'order': UseCaseInterfaceRelation.order + 1})
        relation = UseCaseInterfaceRelation(use_case_id=use_case_id, interface_id=interface_id, order=order)
        session.add(relation)
        session.flush()
        return relation.id


def get_relation(**kwargs):
    """
    根据传入参数不同获取不同信息：
        use_case_id：获取某个use_case包含的interface
        interface_id：获取某个interface关联的use_case
    :param use_case_id:
    :return:
    """
    with session_scope() as session:
        query = session\
            .query(UseCaseInterfaceRelation)\
            .filter_by(**kwargs)\
            .filter_by(status=1)
        session.expunge_all()
    relation_list = [s_relation.to_dict() for s_relation in query]
    return relation_list


def del_relation(relation_id):
    """
    删除use_case与interface关系
    如果有order大于当前删除order的，全部减一
    :param relation_id:           relation id
    :return:
    """
    with session_scope() as session:
        relation = session.query(UseCaseInterfaceRelation).filter_by(id=relation_id).one()
        current_order = relation.order
        use_case_id = relation.use_case_id
        session.query(UseCaseInterfaceRelation).filter_by(id=relation_id).update({'status': 0})
        session\
            .query(UseCaseInterfaceRelation)\
            .filter_by(use_case_id=use_case_id)\
            .filter(UseCaseInterfaceRelation.order > current_order)\
            .update({'order': UseCaseInterfaceRelation.order - 1})


def reorder_relation(relation_id, new_order):
    """
    调整某个已有interface的order
    同时将其他影响范围内的interface的order全部加一或者减一
    :return:
    """
    with session_scope() as session:
        relation = session.query(UseCaseInterfaceRelation).filter_by(id=relation_id).one()
        current_order = relation.order
        use_case_id = relation.use_case_id
        if current_order == new_order:
            return
        elif current_order < new_order:
            session\
                .query(UseCaseInterfaceRelation)\
                .filter_by(use_case_id=use_case_id)\
                .filter(UseCaseInterfaceRelation.order > current_order)\
                .filter(UseCaseInterfaceRelation.order <= new_order)\
                .update({'order': UseCaseInterfaceRelation.order - 1})
        elif current_order > new_order:
            session\
                .query(UseCaseInterfaceRelation)\
                .filter_by(use_case_id=use_case_id)\
                .filter(UseCaseInterfaceRelation.order < current_order)\
                .filter(UseCaseInterfaceRelation.order >= new_order)\
                .update({'order': UseCaseInterfaceRelation.order + 1})
        session\
            .query(UseCaseInterfaceRelation)\
            .filter_by(id=relation_id)\
            .update({'order': new_order})


def add_case_parameter_relation(**kwargs):
    """
    添加用例关联参数信息
    :param kwargs:
    :return:
    """
    with session_scope() as session:
        use_case_parameter = UseCaseParameterRelation(**kwargs)
        session.add(use_case_parameter)


def get_case_parameter_relation(**kwargs):
    """
    查询用例关联参数信息
    :param kwargs:
    :return:
    """
    with session_scope() as session:
        query = session.query(UseCaseParameterRelation).filter_by(**kwargs).filter_by(status=1)
        session.expunge_all()
    parameter_list = [s_param.to_dict() for s_param in query]
    return parameter_list


def modify_case_parameter_relation(**kwargs):
    """
    更新用例关联参数信息
    :param kwargs:
    :return:
    """
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(UseCaseParameterRelation).filter_by(id=id).update(kwargs)


def del_case_parameter_relation(**kwargs):
    """
    更新用例关联参数信息
    :param kwargs:
    :return:
    """
    with session_scope() as session:
        session.query(UseCaseParameterRelation).filter_by(**kwargs).update({'status':0})



