from application import session_scope
from application.model.interface import Interface


def add_interface(**kwargs):
    with session_scope() as session:
        interface = Interface(**kwargs)
        session.add(interface)


def get_interface(**kwargs):
    with session_scope() as session:
        interface_list = session.query(Interface).filter_by(**kwargs)
        session.expunge_all()
    return interface_list


def modify_interface(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Interface).filter_by(id=id).update(kwargs)


def del_interface(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Interface).filter_by(id=id).update({'status': 0})
