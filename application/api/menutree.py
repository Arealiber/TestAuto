# -*- coding:utf-8
from application import session_scope
from application.model.menutree import *


def add_business_line(**kwargs):
    with session_scope() as session:
        business_line = BusinessLine(**kwargs)
        session.add(business_line)
        session.flush()
        return business_line.id


def add_system_line(**kwargs):
    with session_scope() as session:
        system_line = SystemLine(**kwargs)
        session.add(system_line)
        session.flush()
        return system_line.id


def add_function_line(**kwargs):
    with session_scope() as session:
        function_line = FunctionLine(**kwargs)
        session.add(function_line)
        session.flush()
        return function_line.id


def query_business_line(**kwargs):
    with session_scope() as session:
        query = session.query(BusinessLine).filter_by(**kwargs).filter_by(status=1)
    business_list = [business.to_dict() for business in query]
    return business_list


def query_system_line(**kwargs):
    with session_scope() as session:
        query = session.query(SystemLine).filter_by(**kwargs).filter_by(status=1)
    system_line_list = [system_line.to_dict() for system_line in query]
    return system_line_list


def query_function_line(**kwargs):
    with session_scope() as session:
        query = session.query(FunctionLine).filter_by(**kwargs).filter_by(status=1)
    function_line_list = [function_line.to_dict() for function_line in query]
    return function_line_list


def query_all_line_relation(**kwargs):
    with session_scope() as session:
        system_info = session.query(SystemLine).filter_by(**kwargs).filter_by(status=1)
        function_line_list = [system_line.to_dict() for system_line in system_info]
        return function_line_list







