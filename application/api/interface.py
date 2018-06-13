# -*- coding: utf-8 -*-
from application import session_scope
from application.model.interface import Interface


def add_interface(**kwargs):
    with session_scope() as session:
        interface = Interface(**kwargs)
        session.add(interface)
        session.flush()
        return interface.id


def get_interface(**kwargs):
    with session_scope() as session:
        query = session.query(Interface).filter_by(**kwargs).filter_by(status=1).order_by(Interface.update_time.desc())
    interface_list = [interface.to_dict() for interface in query]
    return interface_list


def query_single_interface(interface_id):
    with session_scope() as session:
        query = session.query(Interface).filter_by(id=interface_id)
    interface_info = [interface.to_dict() for interface in query][0]
    return interface_info


def query_interface_count():
    with session_scope() as session:
        interface_count = session.query(Interface).filter_by(status=1).count()
    return interface_count


def modify_interface(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Interface).filter_by(id=id).update(kwargs)


def del_interface(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Interface).filter_by(id=id).update({'status': 0})
