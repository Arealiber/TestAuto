# -*- coding:utf-8 -*-
from datetime import datetime
from application import engine
from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, Float, Boolean


meta = MetaData(bind=engine)
batch_run_log_table = {}
use_case_run_log_table = {}
interface_run_log_table = {}


# 用例脚本的运行日记表
def get_batch_run_log_table(table_name):
    table = batch_run_log_table.get(table_name)
    if table is None:
        table = Table('batch_run_log_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('batch_id', Integer, nullable=False),
                      Column('use_case_count', Integer, nullable=False),
                      Column('pass_rate', Integer, default=-1, nullable=False),  # 百分比，-1表示未执行完成
                      Column('start_time', DateTime, nullable=False),
                      Column('end_time', DateTime),
                      Column('cost_time', Float),
                      Column('create_time', DateTime, default=datetime.utcnow, nullable=False)
                      )
        table.create(checkfirst=True)
        batch_run_log_table[table_name] = table
    return table


# 用例脚本的运行日记表
def get_use_case_run_log_table(table_name):
    table = use_case_run_log_table.get(table_name)
    if table is None:
        table = Table('use_case_run_log_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('batch_run_log_id', Integer),
                      Column('use_case_id', Integer, nullable=False),
                      Column('is_pass', Boolean),
                      Column('start_time', DateTime, nullable=False),
                      Column('end_time', DateTime),
                      Column('create_time', DateTime, default=datetime.utcnow),
                      Column('cost_time', Float, nullable=False)
                      )
        table.create(checkfirst=True)
        use_case_run_log_table[table_name] = table
    return table


# 接口的运行日记表
def get_interface_run_log_table(table_name):
    table = interface_run_log_table.get(table_name)
    if table is None:
        table = Table('interface_run_log_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('use_case_run_log_id', Integer, nullable=False),
                      Column('interface_id', Integer, nullable=False),
                      Column('r_code', String(1000), nullable=False),
                      Column('r_header', String(1000), nullable=False),
                      Column('r_payload', String(1000), nullable=False),
                      Column('is_pass', Boolean, nullable=False),
                      Column('cost_time', Float, nullable=False),
                      Column('start_time', DateTime, nullable=False),
                      Column('end_time', DateTime, nullable=False)
                      )
        table.create(checkfirst=True)
        interface_run_log_table[table_name] = table
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
