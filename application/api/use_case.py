# -*- coding:utf-8 -*-
from application import session_scope
from application.model.use_case import UseCase


def add_use_case(**kwargs):
    with session_scope() as session:
        use_case = UseCase(**kwargs)
        session.add(use_case)
        return use_case.use_case_name


def get_use_case(**kwargs):
    with session_scope() as session:
        use_case_list = session.query(UseCase).filter_by(**kwargs).filter_by(status=1)
        session.expunge_all()
        return use_case_list


def modify_use_case(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        use_case = session.query(UseCase).filter_by(id=id)
        use_case.filter_by(id=id).update(kwargs)
        return use_case.filter_by(id=id).first().use_case_name


def del_use_case(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        use_case = session.query(UseCase)
        use_case.filter_by(id=id).update({'status': 0})
        return use_case.filter_by(id=id).first().use_case_name


