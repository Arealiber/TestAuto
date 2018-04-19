# -*- coding:utf-8 -*-
import time
import importlib
from application import session_scope
from application.model.run_log import UseCaseRunLog, RelationInterfaceRunLog

current_time = time.strftime('%Y%m')


def reload_import_module(imp_package_path, **kwargs):
    imp_module = importlib.import_module('.', imp_package_path)
    importlib.reload(imp_module)
    module_list = []
    for arg in kwargs.values():
        module_list.append(getattr(imp_module, arg))
    return tuple(module_list)


if UseCaseRunLog.run_time == current_time:
    UseCaseRunLog, RelationInterfaceRunLog = reload_import_module('application.model.run_log',
                                                                  UseCaseRunLog='UseCaseRunLog',
                                                                  RelationInterfaceRunLog='RelationInterfaceRunLog')


def add_use_case_run_log(**kwargs):
    with session_scope() as session:
        use_case_run_log = UseCaseRunLog(**kwargs)
        session.add(use_case_run_log)
        session.flush()


def get_use_case_run_log(**kwargs):
    with session_scope() as session:
        query = session.query(UseCaseRunLog).filter_by(**kwargs).filter_by(status=1)
    use_case_run_log_list = [use_case.to_dict() for use_case in query]
    return use_case_run_log_list


def query_run_log_count(**kwargs):
    with session_scope() as session:
        run_log_count = session.query(UseCaseRunLog).filter_by(**kwargs).filter_by(status=1).count()
    return run_log_count


def add_relation_interface_run_log(**kwargs):
    with session_scope() as session:
        relation_interface_run_log = RelationInterfaceRunLog(**kwargs)
        session.add(relation_interface_run_log)
        session.flush()


def get_relation_interface_run_log(**kwargs):
    with session_scope() as session:
        query = session.query(RelationInterfaceRunLog).filter_by(**kwargs).filter_by(status=1)
        relation_interface_run_log_list = [relation_interface_run_log.to_dict() for relation_interface_run_log in query]
        return relation_interface_run_log_list


def query_relation_interface_run_log_count(**kwargs):
    with session_scope() as session:
        run_log_count = session.query(RelationInterfaceRunLog).filter_by(**kwargs).filter_by(status=1).count()
    return run_log_count





