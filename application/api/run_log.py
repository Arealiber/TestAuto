# -*- coding: utf-8 -*-
from application.util.decorator import *
from application.model.run_log import *


@table_decorator
def add_batch_run_log(**kwargs):
    table = get_batch_run_log_table(kwargs.pop('table_time'))
    sql = table.insert(kwargs)
    return exec_change(sql)


@table_decorator
def get_multi_batch_run_log_info(**kwargs):
    query_table_time = kwargs.pop('table_time')
    batch_id = kwargs.get('batch_id')
    limit = kwargs.get('limit')
    table_name_list = query_table_time if isinstance(query_table_time, list) else query_table_time.split(',')
    ret = []
    for table_name in table_name_list:
        table = get_batch_run_log_table(table_name)
        if batch_id:
            batch_list = [batch_id] if not isinstance(batch_id, list) else batch_id
            sql = table.select().where(table.c.batch_id.in_(batch_list))
        else:
            sql = table.select()
        if limit:
            sql.limit(limit)
        ret += exec_query(sql, is_list=True)
    return ret


@table_decorator
def get_use_case_run_log_table(**kwargs):
    table = get_use_case_run_log_table(kwargs.pop('table_time'))
    sql = table.insert(kwargs)
    return exec_change(sql)


@table_decorator
def get_interface_run_log_table(**kwargs):
    table = get_interface_run_log_table(kwargs.pop('table_time'))
    sql = table.insert(kwargs)
    return exec_change(sql)
