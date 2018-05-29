# -*- coding: utf-8 -*-
from sqlalchemy import func, select, desc
from application.util.decorator import *
from application.model.report import *


@min_table_decorator
def add_minutes_report(**kwargs):
    table = get_minutes_report_table(kwargs.pop('min_table_name')[0])
    sql = table.insert(kwargs)
    return exec_change(sql).inserted_primary_key[0]


@min_table_decorator
def get_minutes_report(**kwargs):
    table_name_fix_lst = kwargs.pop('min_table_name')
    batch_run_log_id = kwargs.get('batch_run_log_id')
    from_time = kwargs.get('from_time')
    to_time = kwargs.get('to_time')
    count = 0
    for table_name in table_name_fix_lst:
        table = get_minutes_report_table(table_name)
        sql = select([func.count()]).select_from(table)
        if len(table_name_fix_lst) == 1 and to_time:
            sql = sql.where(table.c.start_time.__le__(to_time))
            if from_time:
                sql = sql.where(table.c.start_time.__ge__(from_time))
        elif table_name == table_name_fix_lst[0] and from_time:
            sql = sql.where(table.c.start_time.__ge__(from_time))
        elif table_name == table_name_fix_lst[-1] and to_time:
            sql = sql.where(table.c.start_time.__le__(to_time))
        if batch_run_log_id:
            sql = sql.where(table.c.batch_run_log_id == batch_run_log_id)

        count += exec_query(sql, is_list=True)[0]['count_1']
    return count


