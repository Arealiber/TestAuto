# -*- coding: utf-8 -*-
from application.util.decorator import *
from application.model import run_log as RunLogObj
from application.model.run_log import *


@table_decorator
def add_batch_run_log(**kwargs):
    table = get_batch_run_log_table(kwargs.pop('table_name_fix_lst')[0])
    sql = table.insert(kwargs)
    return exec_change(sql).inserted_primary_key[0]


@table_decorator
def get_multi_batch_run_log_info(**kwargs):
    table_name_fix_lst = kwargs.pop('table_name_fix_lst')
    batch_id = kwargs.get('batch_id')
    limit = kwargs.get('limit')
    from_time = kwargs.get('from_time')
    to_time = kwargs.get('to_time')
    ret = []
    for table_name in table_name_fix_lst:
        table = get_batch_run_log_table(table_name)

        batch_list = [batch_id] if not isinstance(batch_id, list) else batch_id

        if len(table_name_fix_lst) == 1 and to_time:
            sql = table.select().where(table.c.end_time.__le__(to_time))
            if from_time:
                sql.where(table.c.end_time.__ge__(from_time))
        elif table_name == table_name_fix_lst[0] and from_time:
            sql = table.select().where(table.c.end_time.__ge__(from_time))
        elif table_name == table_name_fix_lst[-1] and to_time:
            sql = table.select().where(table.c.end_time.__le__(to_time))
        else:
            sql = table.select()
        if batch_id:
            sql = sql.where(table.c.batch_id.in_(batch_list))
        if limit:
            sql.limit(limit)
        ret += exec_query(sql, is_list=True)
    return ret


@table_decorator
def modify_batch_run_log(**kwargs):
    table = get_batch_run_log_table(kwargs.pop('table_name_fix_lst')[0])
    id = kwargs.pop('id')
    sql = table.update(table.c.id == id).values(**kwargs)
    return exec_change(sql)


@table_decorator
def add_use_case_run_log(**kwargs):
    table = get_use_case_run_log_table(kwargs.pop('table_name_fix_lst')[0])
    sql = table.insert(kwargs)
    return exec_change(sql).inserted_primary_key[0]


@table_decorator
def modify_use_case_run_log(**kwargs):
    table = get_use_case_run_log_table(kwargs.pop('table_name_fix_lst')[0])
    id = kwargs.pop('id')
    sql = table.update(table.c.id == id).values(**kwargs)
    return exec_change(sql)


@table_decorator
def get_use_case_run_log(**kwargs):
    table_name_fix_lst = kwargs.pop('table_name_fix_lst')
    use_case_id = kwargs.get('use_case_id')
    limit = kwargs.get('limit')
    from_time = kwargs.get('from_time')
    to_time = kwargs.get('to_time')
    ret = []
    for table_name in table_name_fix_lst:
        table = get_use_case_run_log_table(table_name)
        use_case_list = [use_case_id] if not isinstance(use_case_id, list) else use_case_id
        if len(table_name_fix_lst) == 1 and to_time:
            sql = table.select().where(table.c.end_time.__le__(to_time))
            if from_time:
                sql.where(table.c.end_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[0] and from_time:
            sql = table.select().where(table.c.end_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[-1] and to_time:
            sql = table.select().where(table.c.end_time.__le__(to_time))

        else:
            sql = table.select()
        if use_case_id:
            sql = sql.where(table.c.use_case_id.in_(use_case_list))
        if limit:
            sql.limit(limit)
        ret += exec_query(sql, is_list=True)
    return ret


@table_decorator
def add_interface_run_log(**kwargs):
    table = get_interface_run_log_table(kwargs.pop('table_name_fix_lst')[0])
    sql = table.insert(kwargs)
    return exec_change(sql).inserted_primary_key[0]


@table_decorator
def get_interface_run_log(**kwargs):
    table_name_fix_lst = kwargs.pop('table_name_fix_lst')
    interface_id = kwargs.get('interface_id')
    limit = kwargs.get('limit')
    from_time = kwargs.get('from_time')
    to_time = kwargs.get('to_time')
    ret = []
    for table_name in table_name_fix_lst:
        table = get_interface_run_log_table(table_name)
        if interface_id:
            interface_list = [interface_id] if not isinstance(interface_id, list) else interface_id
            if len(table_name_fix_lst) == 1 and to_time:
                sql = table.select().where(table.c.end_time.__le__(to_time)). \
                    where(table.c.interface_id.in_(interface_list))
                if from_time:
                    sql.where(table.c.end_time.__ge__(from_time))

            elif table_name == table_name_fix_lst[0] and from_time:
                sql = table.select().where(table.c.end_time.__ge__(from_time)). \
                    where(table.c.interface_id.in_(interface_list))

            elif table_name == table_name_fix_lst[-1] and to_time:
                sql = table.select().where(table.c.end_time.__le__(to_time)). \
                    where(table.c.interface_id.in_(interface_list))

            else:
                sql = table.select().where(table.c.interface_id.in_(interface_list))
        else:
            sql = table.select()
        if limit:
            sql.limit(limit)
        ret += exec_query(sql, is_list=True)


@table_decorator
def modify_interface_run_log(**kwargs):
    table = get_interface_run_log_table(kwargs.pop('table_name_fix_lst')[0])
    id = kwargs.pop('id')
    sql = table.update(table.c.id == id).values(**kwargs)
    return exec_change(sql).inserted_primary_key[0]




