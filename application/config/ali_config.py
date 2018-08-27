# -*- coding:utf-8 -*-
import os

TIME_FMT = '%Y-%m-%d %H:%M:%S.%f GMT'
QUERY_TIME_FMT = '%Y-%m-%d %H:%M:%S.%f'
TABLE_TIME_FMT = '%Y-%m-%d'
TABLE_FMT = '%Y'
CONSTANT_LEN = 10  # 7 按月分表, 10按日分表

# 报表计算时间间隔 分、天、周、月
MINUTE_TIME_LENGTH = 5
DAY_TIME_LENGTH = 1
WEEK_TIME_LENGTH = 1
MOUTH_TIME_LENGTH = 30
DEFAULT_TIME_LENGTH = 7  # 默认7 个单位（日、周、月）长度

DAY_TIME_FMT = '%Y-%m-%d 00:00:00'
MINUTE_TIME_FMT = '%Y-%m-%d %H:%M:00.000'
MONTH_TIME_FMT = '%Y-%m-00 00:00:00.000'

web_root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))

PROXIES = True
DEBUG = False
HOST = '0.0.0.0'
PORT = 9091

DB_URI = 'mysql://root:123456@127.0.0.1/auto_test'
DB_POOL_SIZE = 5
DB_POOL_RECYCLE = 5
DB_MAX_OVERFLOW = 10
DB_ECHO = False

# 正式环境内部权限系统
SYSTEM_ID = '42'

# redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_AUTH = '123456'
