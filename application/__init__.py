import os
import sys
import gc
from contextlib import contextmanager
from importlib import import_module
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.config import default

web_root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

app = Flask(
    __name__,
    static_folder=os.path.abspath(os.path.join(web_root, 'static')),
    static_url_path="",
    template_folder=os.path.abspath(os.path.join(web_root, 'templates'))
)

# 设置加载
app.config.from_object(default)
if len(sys.argv) > 1:
    extra_config = import_module('application.config.%s' % sys.argv[1])
    app.config.from_object(extra_config)

# for session
app.secret_key = 'RFmoIw6P6B9LE5otg9ba7iyoXm5PkUM0s8KnV3cr'

# SQLAlchemy engine
engine = create_engine(app.config['DB_URI'] + '?charset=utf8',
                       encoding='utf-8',
                       convert_unicode=True,
                       pool_recycle=app.config['DB_POOL_RECYCLE'],
                       pool_size=app.config['DB_POOL_SIZE'],
                       max_overflow=app.config['DB_MAX_OVERFLOW'],
                       echo=app.config['DB_ECHO'],
                       pool_pre_ping=True)

# SQLAlchemy session
session_factory = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        gc.collect()
