# -*- coding: utf-8 -*-
from application import session_scope
from application.model.interface import Interface


def add_interface(**kwargs):
    with session_scope() as session:
        interface = Interface(**kwargs)
        session.add(interface)


def get_interface(**kwargs):
    with session_scope() as session:
        query = session.query(Interface).filter_by(**kwargs).filter_by(status=1)
    interface_list = [interface.to_dict() for interface in query]
    return interface_list


def modify_interface(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Interface).filter_by(id=id).update(kwargs)


def del_interface(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Interface).filter_by(id=id).update({'status': 0})
