from application import session_scope
from application.model.parameter import Parameter


def add_parameter(**kwargs):
    with session_scope() as session:
        parameter = Parameter(**kwargs)
        session.add(parameter)


def get_parameter(**kwargs):
    with session_scope() as session:
        parameter_list = session.query(Parameter).filter_by(**kwargs).filter_by(status=1)
        session.expunge_all()
    return parameter_list


def modify_parameter(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Parameter).filter_by(id=id).update(kwargs)


def del_parameter(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Parameter).filter_by(id=id).update({'status': 0})
