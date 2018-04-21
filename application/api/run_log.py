# -*- coding: utf-8 -*-
from application.model.run_log import *


def add_batch_run_log(**kwargs):
    print('***********', kwargs)
    table_col = kwargs
    table = get_batch_run_log_table(table_col.pop('table_name'))
    sql = table.insert(table_col)
    return exec_change(sql)
