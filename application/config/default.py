# -*- coding:utf-8 -*-
import os

TIME_FMT = '%Y-%m-%d %H:%M:%S.%f GMT'
QUERY_TIME_FMT = '%Y-%m-%d %H:%M:%S.%f'
TABLE_TIME_FMT = '%Y-%m-%d'
MIN_TABLE_FMT = '%Y-%m-%d %H:%M'
CONSTANT_LEN = 10  # 7 按月分表, 10按日分表

# 报表计算时间间隔 分、天、周、月
MINUTE_TIME_LENGTH = 5000
DAY_TIME_LENGTH = 1
WEEK_TIME_LENGTH = 5
MOUTH_TIME_LENGTH = 1

web_root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))


DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

DB_URI = 'mysql://hjx:123456@119.29.141.207/auto_test'
DB_POOL_SIZE = 5
DB_POOL_RECYCLE = 5
DB_MAX_OVERFLOW = 10
DB_ECHO = False

# 内部权限系统
SYSTEM_ID = '106'
