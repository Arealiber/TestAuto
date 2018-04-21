# -*- coding: utf-8 -*-
from application.util.decorator import *
from application.model.run_log import *


@table_decorator
def add_batch_run_log(**kwargs):
    table = get_batch_run_log_table(kwargs.pop('table_time'))
    sql = table.insert(kwargs)
    return exec_change(sql)
