# -*- coding:utf-8 -*-
import time
from datetime import datetime
from application import engine
from application.util.redis_lock import deco, RedisLock
from sqlalchemy import Table, MetaData, Column, Integer, String, Float, Boolean, TEXT
from sqlalchemy.dialects.mysql import TIMESTAMP


meta = MetaData(bind=engine)
batch_run_log_table = {}
use_case_run_log_table = {}
interface_run_log_table = {}


# 用例脚本的运行日记表
def get_batch_run_log_table(table_name):
    table = batch_run_log_table.get('batch_run_log_{0}'.format(table_name), None)
    if table is None:
        table = Table('batch_run_log_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('batch_id', Integer, nullable=False),
                      Column('use_case_count', Integer, nullable=False),
                      Column('pass_rate', Integer, default=-1, nullable=False),  # 百分比，-1表示未执行完成
                      Column('start_time', TIMESTAMP(fsp=3), default=datetime.utcnow),
                      Column('end_time', TIMESTAMP(fsp=3)),
                      Column('cost_time', Float, default=0),
                      Column('create_time', TIMESTAMP(fsp=3), default=datetime.utcnow, nullable=False),
                      autoload=True,
                      extend_existing=True,
                      )
        create_table(table, engine)
        batch_run_log_table['batch_run_log_{0}'.format(table_name)] = table
    return table


# 用例脚本的运行日记表
def get_use_case_run_log_table(table_name):
    table = use_case_run_log_table.get('use_case_run_log_{0}'.format(table_name), None)
    if table is None:
        table = Table('use_case_run_log_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('batch_run_log_id', Integer),
                      Column('use_case_id', Integer, nullable=False),
                      Column('is_pass', Boolean, default=False),
                      Column('start_time', TIMESTAMP(fsp=3), default=datetime.utcnow),
                      Column('end_time', TIMESTAMP(fsp=3)),
                      Column('create_time', TIMESTAMP(fsp=3), default=datetime.utcnow),
                      Column('cost_time', Float, nullable=False, default=0),
                      Column('auto_run', Boolean, default=False),
                      autoload=True,
                      extend_existing=True,
                      )
        create_table(table, engine)
        use_case_run_log_table['batch_run_log_{0}'.format(table_name)] = table
    return table


# 接口的运行日记表
def get_interface_run_log_table(table_name):
    table = interface_run_log_table.get('interface_run_log_{0}'.format(table_name), None)
    if table is None:
        table = Table('interface_run_log_{0}'.format(table_name), meta,
                      Column('id', Integer, primary_key=True),
                      Column('use_case_run_log_id', Integer, nullable=False),
                      Column('interface_id', Integer, nullable=False),
                      Column('s_header', TEXT),  # 发送的header
                      Column('s_payload', TEXT),  # 发送的payload
                      Column('r_code', String(10)),  # 返回的HTTP code
                      Column('r_header', TEXT),  # 返回的HTTP header
                      Column('r_payload', TEXT),  # 返回的json
                      Column('is_pass', Boolean, nullable=False),
                      Column('cost_time', Float, nullable=False, default=0),
                      Column('start_time', TIMESTAMP(fsp=3), default=datetime.utcnow),
                      Column('end_time', TIMESTAMP(fsp=3), nullable=False),
                      Column('error_message', String(2000)),
                      autoload=True,
                      extend_existing=True,
                      )
        create_table(table, engine)
        interface_run_log_table['batch_run_log_{0}'.format(table_name)] = table
    return table


@deco(RedisLock('run_log_lock'))
def create_table(table, bind):
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
