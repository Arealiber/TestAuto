# -*- coding:utf-8 -*-
from datetime import datetime
from application.config.default import TIME_FMT


def table_decorator(func):
    def wrapper(**kwargs):
        fmt_str = (datetime.strftime(datetime.now(), TIME_FMT))
        kwargs.update({'table_time': fmt_str}) if 'table_time' not in kwargs else None
        return func(**kwargs)
    return wrapper


