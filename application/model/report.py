# -*- coding:utf-8 -*-
import time
from datetime import datetime
from application import engine
from application.util.redis_lock import deco, RedisLock
from sqlalchemy import Table, MetaData, Column, Integer, String, Float, Boolean, TEXT, DateTime
from sqlalchemy.dialects.mysql import TIMESTAMP


meta = MetaData(bind=engine)


# 用例脚本的5分钟报表
def get_minutes_report_table(table_name):
    table = Table('report_minute_{0}'.format(table_name), meta,
                  Column('id', Integer, primary_key=True),
                  Column('function_id', Integer, nullable=False),
                  Column('run_count', Integer, nullable=False),
                  Column('success_count', Integer, nullable=False),
                  Column('fail_count', Integer, nullable=False),
                  Column('pass_rate', Float, nullable=False),
                  Column('sum_time', Float),
                  Column('average_time', Float),
                  Column('max_time', Float),
                  Column('create_time', DateTime, default=datetime.now, nullable=False),
                  extend_existing=True,
                  )
    create_table(table, engine, 'report_minute_{0}'.format(table_name))
    return table


# 用例脚本的日报表
def get_day_report_table(table_name):
    table = Table('report_day_{0}'.format(table_name), meta,
                  Column('id', Integer, primary_key=True),
                  Column('function_id', Integer, nullable=False),
                  Column('run_count', Integer, nullable=False),
                  Column('success_count', Integer, nullable=False),
                  Column('fail_count', Integer, nullable=False),
                  Column('pass_rate', Float, nullable=False),
                  Column('sum_time', Float),
                  Column('average_time', Float),
                  Column('max_time', Float),
                  Column('create_time', DateTime, default=datetime.now, nullable=False),
                  extend_existing=True,
                  )
    create_table(table, engine, 'report_day_{0}'.format(table_name))
    return table


# 用例脚本的周报表
def get_week_report_table(table_name):
    table = Table('report_week_{0}'.format(table_name), meta,
                  Column('id', Integer, primary_key=True),
                  Column('function_id', Integer, nullable=False),
                  Column('run_count', Integer, nullable=False),
                  Column('success_count', Integer, nullable=False),
                  Column('fail_count', Integer, nullable=False),
                  Column('pass_rate', Float, nullable=False),
                  Column('sum_time', Float),
                  Column('average_time', Float),
                  Column('max_time', Float),
                  Column('create_time', DateTime, default=datetime.now, nullable=False),
                  extend_existing=True,
                  )
    create_table(table, engine, 'report_week_{0}'.format(table_name))
    return table


# 用例脚本的月报表
def get_month_report_table(table_name):
    table = Table('report_month_{0}'.format(table_name), meta,
                  Column('id', Integer, primary_key=True),
                  Column('function_id', Integer, nullable=False),
                  Column('run_count', Integer, nullable=False),
                  Column('success_count', Integer, nullable=False),
                  Column('fail_count', Integer, nullable=False),
                  Column('pass_rate', Float, nullable=False),
                  Column('sum_time', Float),
                  Column('average_time', Float),
                  Column('max_time', Float),
                  Column('create_time', DateTime, default=datetime.now, nullable=False),
                  extend_existing=True,
                  )
    create_table(table, engine, 'report_month_{0}'.format(table_name))
    return table


def create_table(table, bind, table_name):
    if table_name not in meta.tables:
        lock_create_table(table, bind, check_first=True)
    else:
        table.create(bind=engine, checkfirst=True)


@deco(RedisLock('table_lock'))
def lock_create_table(table, bind):
    table.create(bind=bind, checkfirst=True)


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
    retry = 3
    conn = trans = None
    while retry > 0:
        try:
            conn = engine.connect()
            trans = conn.begin()
            break
        except Exception as e:
            print(str(e))
            retry -= 1
            if not retry:
                raise e
        time.sleep(1)
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
