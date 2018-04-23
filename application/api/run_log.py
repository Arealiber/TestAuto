# -*- coding: utf-8 -*-
from application.util.decorator import *
from application.model.run_log import *


@table_decorator
def add_batch_run_log(**kwargs):
    table = get_batch_run_log_table(kwargs.pop('table_name_fix_lst')[0])
    sql = table.insert(kwargs)
    return exec_change(sql)


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
        if batch_id:
            batch_list = [batch_id] if not isinstance(batch_id, list) else batch_id
            if len(table_name_fix_lst) == 1 and to_time:
                sql = table.select().where(table.c.end_time.__le__(to_time)).where(table.c.batch_id.in_(batch_list))
                if from_time:
                    sql.where(table.c.end_time.__ge__(from_time))

            elif table_name == table_name_fix_lst[0] and from_time:
                sql = table.select().where(table.c.end_time.__ge__(from_time)).\
                    where(table.c.batch_id.in_(batch_list))

            elif table_name == table_name_fix_lst[-1] and to_time:
                sql = table.select().where(table.c.end_time.__le__(to_time)). \
                    where(table.c.batch_id.in_(batch_list))

            else:
                sql = table.select().where(table.c.batch_id.in_(batch_list))
        else:
            sql = table.select()
        if limit:
            sql.limit(limit)
        ret += exec_query(sql, is_list=True)
    return ret


@table_decorator
def add_use_case_run_log(**kwargs):
    table = get_use_case_run_log_table(kwargs.pop('table_name_fix_lst')[0])
    sql = table.insert(kwargs)
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
        table = get_batch_run_log_table(table_name)
        if use_case_id:
            use_case_list = [use_case_id] if not isinstance(use_case_id, list) else use_case_id
            if len(table_name_fix_lst) == 1 and to_time:
                sql = table.select().where(table.c.end_time.__le__(to_time)).\
                    where(table.c.use_case_id.in_(use_case_list))
                if from_time:
                    sql.where(table.c.end_time.__ge__(from_time))

            elif table_name == table_name_fix_lst[0] and from_time:
                sql = table.select().where(table.c.end_time.__ge__(from_time)). \
                    where(table.c.use_case_id.in_(use_case_list))

            elif table_name == table_name_fix_lst[-1] and to_time:
                sql = table.select().where(table.c.end_time.__le__(to_time)). \
                    where(table.c.use_case_id.in_(use_case_list))

            else:
                sql = table.select().where(table.c.use_case_id.in_(use_case_list))
        else:
            sql = table.select()
        if limit:
            sql.limit(limit)
        ret += exec_query(sql, is_list=True)
    return ret


@table_decorator
def add_interface_run_log(**kwargs):
    table = get_interface_run_log_table(kwargs.pop('table_name_fix_lst')[0])
    sql = table.insert(kwargs)
    return exec_change(sql)


@table_decorator
def get_interface_run_log(**kwargs):
    table = get_use_case_run_log_table(kwargs.pop('table_time')[0])
    sql = table.insert(kwargs)
    return exec_change(sql)


