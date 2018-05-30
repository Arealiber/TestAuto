# -*- coding: utf-8 -*-
from sqlalchemy import func, select, desc
from application.util.decorator import *
from application.model.report import *


@report_table_decorator
def add_minutes_report(**kwargs):
    table = get_minutes_report_table(kwargs.pop('table_name')[0])
    sql = table.insert(kwargs)
    return exec_change(sql).inserted_primary_key[0]


@report_table_decorator
def get_minutes_report_info(**kwargs):
    table_name_fix_lst = kwargs.pop('table_name')
    use_case_id = kwargs.get('use_case_id')
    from_time = kwargs.get('from_time')
    to_time = kwargs.get('to_time')
    page_index = kwargs.get('pageIndex')
    page_size = kwargs.get('pageSize')
    page_index = int(page_index) if page_index else None
    page_size = int(page_size) if page_size else None
    if page_size:
        index = (page_index - 1) * page_size
    else:
        index = -1
    total_count = 0
    ret = []
    for table_name in table_name_fix_lst:
        table = get_minutes_report_table(table_name)
        sql = table.select()
        count_sql = select([func.count()]).select_from(table)
        use_case_list = [use_case_id] if not isinstance(use_case_id, list) else use_case_id
        if len(table_name_fix_lst) == 1 and to_time:
            sql = sql.where(table.c.create_time.__le__(to_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))
            if from_time:
                sql = sql.where(table.c.create_time.__ge__(from_time))
                count_sql = count_sql.where(table.c.create_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[0] and from_time:
            sql = sql.where(table.c.create_time.__ge__(from_time))
            count_sql = count_sql.where(table.c.create_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[-1] and to_time:
            sql = sql.where(table.c.create_time.__le__(to_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))

        if use_case_id:
            sql = sql.where(table.c.use_case_id.in_(use_case_list)).order_by(desc(table.c.create_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))
        else:
            sql = sql.order_by(desc(table.c.create_time))
        if not page_size:
            ret += exec_query(sql, is_list=True)
            continue
        count = exec_query(count_sql, is_list=True)[0]['count_1']
        total_count += count
        limit = page_size - len(ret)
        if limit == 0:
            break
        if index >= total_count:
            continue
        elif index >= total_count - count - 1:
            offset_num = count - (total_count - index)
            index += total_count - index
        else:
            offset_num = 0
            sql = sql.offset(offset_num).limit(limit)
            ret += exec_query(sql, is_list=True)
            break
        sql = sql.offset(offset_num).limit(limit)
        ret += exec_query(sql, is_list=True)
    return ret


@report_table_decorator
def add_day_report(**kwargs):
    table = get_day_report_table(kwargs.pop('table_name')[0])
    sql = table.insert(kwargs)
    return exec_change(sql).inserted_primary_key[0]


@report_table_decorator
def get_day_report_info(**kwargs):
    table_name_fix_lst = kwargs.pop('table_name')
    use_case_id = kwargs.get('use_case_id')
    from_time = kwargs.get('from_time')
    to_time = kwargs.get('to_time')
    page_index = kwargs.get('pageIndex')
    page_size = kwargs.get('pageSize')
    page_index = int(page_index) if page_index else None
    page_size = int(page_size) if page_size else None
    if page_size:
        index = (page_index - 1) * page_size
    else:
        index = -1
    total_count = 0
    ret = []
    for table_name in table_name_fix_lst:
        table = get_day_report_table(table_name)
        sql = table.select()
        count_sql = select([func.count()]).select_from(table)
        use_case_list = [use_case_id] if not isinstance(use_case_id, list) else use_case_id
        if len(table_name_fix_lst) == 1 and to_time:
            sql = sql.where(table.c.create_time.__le__(to_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))
            if from_time:
                sql = sql.where(table.c.create_time.__ge__(from_time))
                count_sql = count_sql.where(table.c.create_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[0] and from_time:
            sql = sql.where(table.c.create_time.__ge__(from_time))
            count_sql = count_sql.where(table.c.create_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[-1] and to_time:
            sql = sql.where(table.c.create_time.__le__(to_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))

        if use_case_id:
            sql = sql.where(table.c.use_case_id.in_(use_case_list)).order_by(desc(table.c.create_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))
        else:
            sql = sql.order_by(desc(table.c.create_time))
        if not page_size:
            ret += exec_query(sql, is_list=True)
            continue
        count = exec_query(count_sql, is_list=True)[0]['count_1']
        total_count += count
        limit = page_size - len(ret)
        if limit == 0:
            break
        if index >= total_count:
            continue
        elif index >= total_count - count - 1:
            offset_num = count - (total_count - index)
            index += total_count - index
        else:
            offset_num = 0
            sql = sql.offset(offset_num).limit(limit)
            ret += exec_query(sql, is_list=True)
            break
        sql = sql.offset(offset_num).limit(limit)
        ret += exec_query(sql, is_list=True)
    return ret


@report_table_decorator
def add_week_report(**kwargs):
    table = get_week_report_table(kwargs.pop('table_name')[0])
    sql = table.insert(kwargs)
    return exec_change(sql).inserted_primary_key[0]


@report_table_decorator
def get_week_report_info(**kwargs):
    table_name_fix_lst = kwargs.pop('table_name')
    use_case_id = kwargs.get('use_case_id')
    from_time = kwargs.get('from_time')
    to_time = kwargs.get('to_time')
    page_index = kwargs.get('pageIndex')
    page_size = kwargs.get('pageSize')
    page_index = int(page_index) if page_index else None
    page_size = int(page_size) if page_size else None
    if page_size:
        index = (page_index - 1) * page_size
    else:
        index = -1
    total_count = 0
    ret = []
    for table_name in table_name_fix_lst:
        table = get_week_report_table(table_name)
        sql = table.select()
        count_sql = select([func.count()]).select_from(table)
        use_case_list = [use_case_id] if not isinstance(use_case_id, list) else use_case_id
        if len(table_name_fix_lst) == 1 and to_time:
            sql = sql.where(table.c.create_time.__le__(to_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))
            if from_time:
                sql = sql.where(table.c.create_time.__ge__(from_time))
                count_sql = count_sql.where(table.c.create_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[0] and from_time:
            sql = sql.where(table.c.create_time.__ge__(from_time))
            count_sql = count_sql.where(table.c.create_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[-1] and to_time:
            sql = sql.where(table.c.create_time.__le__(to_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))

        if use_case_id:
            sql = sql.where(table.c.use_case_id.in_(use_case_list)).order_by(desc(table.c.create_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))
        else:
            sql = sql.order_by(desc(table.c.create_time))
        if not page_size:
            ret += exec_query(sql, is_list=True)
            continue
        count = exec_query(count_sql, is_list=True)[0]['count_1']
        total_count += count
        limit = page_size - len(ret)
        if limit == 0:
            break
        if index >= total_count:
            continue
        elif index >= total_count - count - 1:
            offset_num = count - (total_count - index)
            index += total_count - index
        else:
            offset_num = 0
            sql = sql.offset(offset_num).limit(limit)
            ret += exec_query(sql, is_list=True)
            break
        sql = sql.offset(offset_num).limit(limit)
        ret += exec_query(sql, is_list=True)
    return ret


@report_table_decorator
def add_month_report(**kwargs):
    table = get_month_report_table(kwargs.pop('table_name')[0])
    sql = table.insert(kwargs)
    return exec_change(sql).inserted_primary_key[0]


@report_table_decorator
def get_month_report_info(**kwargs):
    table_name_fix_lst = kwargs.pop('table_name')
    use_case_id = kwargs.get('use_case_id')
    from_time = kwargs.get('from_time')
    to_time = kwargs.get('to_time')
    page_index = kwargs.get('pageIndex')
    page_size = kwargs.get('pageSize')
    page_index = int(page_index) if page_index else None
    page_size = int(page_size) if page_size else None
    if page_size:
        index = (page_index - 1) * page_size
    else:
        index = -1
    total_count = 0
    ret = []
    for table_name in table_name_fix_lst:
        table = get_month_report_table(table_name)
        sql = table.select()
        count_sql = select([func.count()]).select_from(table)
        use_case_list = [use_case_id] if not isinstance(use_case_id, list) else use_case_id
        if len(table_name_fix_lst) == 1 and to_time:
            sql = sql.where(table.c.create_time.__le__(to_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))
            if from_time:
                sql = sql.where(table.c.create_time.__ge__(from_time))
                count_sql = count_sql.where(table.c.create_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[0] and from_time:
            sql = sql.where(table.c.create_time.__ge__(from_time))
            count_sql = count_sql.where(table.c.create_time.__ge__(from_time))

        elif table_name == table_name_fix_lst[-1] and to_time:
            sql = sql.where(table.c.create_time.__le__(to_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))

        if use_case_id:
            sql = sql.where(table.c.use_case_id.in_(use_case_list)).order_by(desc(table.c.create_time))
            count_sql = count_sql.where(table.c.create_time.__le__(to_time))
        else:
            sql = sql.order_by(desc(table.c.create_time))
        if not page_size:
            ret += exec_query(sql, is_list=True)
            continue
        count = exec_query(count_sql, is_list=True)[0]['count_1']
        total_count += count
        limit = page_size - len(ret)
        if limit == 0:
            break
        if index >= total_count:
            continue
        elif index >= total_count - count - 1:
            offset_num = count - (total_count - index)
            index += total_count - index
        else:
            offset_num = 0
            sql = sql.offset(offset_num).limit(limit)
            ret += exec_query(sql, is_list=True)
            break
        sql = sql.offset(offset_num).limit(limit)
        ret += exec_query(sql, is_list=True)
    return ret
