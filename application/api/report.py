# -*- coding: utf-8 -*-
from sqlalchemy import func, select, desc
from application.util.decorator import *
from application.model.report import *


@run_log_table_decorator
def add_minutes_report(**kwargs):
    table = get_minutes_report_table(kwargs.pop('table_name_fix_lst')[0])
    sql = table.insert(kwargs)
    return exec_change(sql).inserted_primary_key[0]

