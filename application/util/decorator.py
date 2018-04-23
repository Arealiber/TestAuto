# -*- coding:utf-8 -*-
from datetime import datetime
from application.config.default import TIME_FMT, QUERY_TIME_FMT, TABLE_TIME_FMT
from dateutil.rrule import rrule, MONTHLY


def table_decorator(func):
    def wrapper(**kwargs):
        fmt_str = (datetime.strftime(datetime.now(), TIME_FMT))
        if not('from_time' in kwargs or 'to_time' in kwargs):
            kwargs.update({'table_name_fix_lst': [fmt_str[:7]]})
        else:
            from_time = kwargs.get('from_time').strip() if kwargs.get('from_time') is not None else None
            to_time = kwargs.get('to_time').strip() if kwargs.get('to_time') is not None else fmt_str.strip()
            if from_time is None:
                dt_table_from_time, dt_table_to_time = multi_strptime(to_time[:7], to_time[:7],
                                                                      str_format=TABLE_TIME_FMT)
            table_name_fix_lst = [dt.strftime(TABLE_TIME_FMT) for dt in rrule(MONTHLY,
                                                                              dtstart=dt_table_from_time,
                                                                              until=dt_table_to_time)]
            dt_from_time, dt_to_time = multi_strptime(from_time, to_time)
            kwargs.update({
                'table_name_fix_lst': table_name_fix_lst,
                'from_time': dt_from_time,
                'to_time': dt_to_time
            })
        return func(**kwargs)
    return wrapper


def multi_strptime(*args, str_format=QUERY_TIME_FMT):
    dt_time = []
    for dt_arg in args:
        if dt_arg is None:
            dt_time.append(None)
            continue
        print(dt_arg)
        dt_time.append(datetime.strptime(dt_arg, str_format))
    return tuple(dt_time)


print(datetime.strftime(datetime.now(), TIME_FMT))

