# -*- coding:utf-8 -*-
import os

rebuild_run_log_table_time = '%Y%m%d'
web_root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))


DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

DB_URI = 'mysql://hjx:123456@119.29.141.207/auto_test'
DB_POOL_SIZE = 100
DB_POOL_RECYCLE = 7200
DB_ECHO = True
