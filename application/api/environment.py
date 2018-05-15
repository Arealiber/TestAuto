# -*- coding: utf-8 -*-
from application import session_scope
from application.model.environment import EnvironmentLine, EnvironmentInfo


def add_environment_line(**kwargs):
    with session_scope() as session:
        environment_line = EnvironmentLine(**kwargs)
        session.add(environment_line)
        session.flush()
        return environment_line.id


def add_environment_line_info(**kwargs):
    with session_scope() as session:
        environment_info = EnvironmentInfo(**kwargs)
        session.add(environment_info)
        session.flush()
        return environment_info.id


def del_environment_line(**kwargs):
    line_id = kwargs.get('id')
    with session_scope() as session:
        session.query(EnvironmentLine).filter_by(id=line_id).delete(synchronize_session=False)


def del_environment_line_info(**kwargs):
    info_id = kwargs.get('id')
    if isinstance(info_id, list):
        info_id = [info_id]
    with session_scope() as session:
        session.query(EnvironmentInfo).filter(EnvironmentInfo.id.in_(info_id)).delete(synchronize_session=False)


def get_environment_line(**kwargs):
    with session_scope() as session:
        query = session.query(EnvironmentLine).filter_by(**kwargs)
        environment_line_list = [line.to_dict() for line in query]
    return environment_line_list


def get_environment_line_info(**kwargs):
    with session_scope() as session:
        query = session.query(EnvironmentInfo).filter_by(**kwargs)
        line_info_list = [line_info.to_dict() for line_info in query]
    return line_info_list


def modify_environment_line(**kwargs):
    line_id = kwargs.pop('id')
    with session_scope() as session:
        session.query(EnvironmentLine).filter_by(id=line_id).update(kwargs)
    return line_id


def modify_environment_line_info(**kwargs):
    info_id = kwargs.pop('id')
    with session_scope() as session:
        session.query(EnvironmentInfo).filter_by(id=info_id).update(kwargs)
    return info_id
