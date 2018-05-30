# -*- coding:utf-8 -*-
from datetime import datetime
from application import engine
from sqlalchemy import Table, MetaData, Column, Integer, String, Float, Boolean, TEXT, DateTime
from sqlalchemy.dialects.mysql import TIMESTAMP


meta = MetaData(bind=engine)
minutes_report_table = {}
day_report_table = {}
week_report_table = {}
month_report_table = {}


# 用例脚本的5分钟报表
def get_minutes_report_table(table_name):
    table = minutes_report_table.get(table_name)
    if table is None:
        table = Table('report_minute_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('use_case_id', Integer, nullable=False),
                      Column('run_count', Integer, nullable=False),
                      Column('success_count', Integer, nullable=False),
                      Column('fail_count', Integer, nullable=False),
                      Column('pass_rate', Float, nullable=False),
                      Column('sum_time', Float),
                      Column('average_time', Float),
                      Column('max_time', Float),
                      Column('create_time', DateTime, default=datetime.utcnow, nullable=False)
                      )
        table.create(checkfirst=True)
        minutes_report_table[table_name] = table
    return table


# 用例脚本的日报表
def get_day_report_table(table_name):
    table = day_report_table.get(table_name)
    if table is None:
        table = Table('report_day_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('use_case_id', Integer, nullable=False),
                      Column('run_count', Integer, nullable=False),
                      Column('success_count', Integer, nullable=False),
                      Column('fail_count', Integer, nullable=False),
                      Column('pass_rate', Float, nullable=False),
                      Column('sum_time', Float),
                      Column('average_time', Float),
                      Column('max_time', Float),
                      Column('create_time', DateTime, default=datetime.utcnow, nullable=False)
                      )
        table.create(checkfirst=True)
        day_report_table[table_name] = table
    return table


# 用例脚本的周报表
def get_week_report_table(table_name):
    table = week_report_table.get(table_name)
    if table is None:
        table = Table('report_week_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('use_case_id', Integer, nullable=False),
                      Column('run_count', Integer, nullable=False),
                      Column('success_count', Integer, nullable=False),
                      Column('fail_count', Integer, nullable=False),
                      Column('pass_rate', Float, nullable=False),
                      Column('average_time', Float),
                      Column('max_time', Float),
                      Column('create_time', DateTime, default=datetime.utcnow, nullable=False)
                      )
        table.create(checkfirst=True)
        week_report_table[table_name] = table
    return table


# 用例脚本的月报表
def get_month_report_table(table_name):
    table = month_report_table.get(table_name)
    if table is None:
        table = Table('report_month_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('use_case_id', Integer, nullable=False),
                      Column('run_count', Integer, nullable=False),
                      Column('success_count', Integer, nullable=False),
                      Column('fail_count', Integer, nullable=False),
                      Column('pass_rate', Float, nullable=False),
                      Column('average_time', Float),
                      Column('max_time', Float),
                      Column('create_time', DateTime, default=datetime.utcnow, nullable=False)
                      )
        table.create(checkfirst=True)
        month_report_table[table_name] = table
    return table


def exec_query(sql, is_list=False):
    conn = engine.connect()
    try:
        ret = []
        for one in conn.execute(sql).fetchall():
            ret.append(dict(one.items()))
        if not is_list:
            return ret if len(ret) != 1 else ret[0]
        return ret
    except Exception as e:
        raise e
    finally:
        conn.close()


def exec_change(*args):
    conn = engine.connect()
    trans = conn.begin()
    try:
        ret = []
        for sql in args:
            ret.append(conn.execute(sql))
        trans.commit()
        return ret if len(ret) != 1 else ret[0]
    except Exception as e:
        trans.rollback()
        raise e
    finally:
        conn.close()


def drop_all():
    meta.reflect(engine)
    meta.drop_all()


def create_all():
    meta.reflect(engine)
    meta.create_all()
