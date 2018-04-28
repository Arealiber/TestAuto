import os
from contextlib import contextmanager
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from application.config import default

web_root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

app = Flask(
    __name__,
    static_folder=os.path.abspath(os.path.join(web_root, 'static')),
    static_url_path="",
    template_folder=os.path.abspath(os.path.join(web_root, 'templates'))
)
app.config.from_object(default)

# SQLAlchemy engine
engine = create_engine(app.config['DB_URI'] + '?charset=utf8',
                       encoding='utf-8',
                       poolclass=NullPool,
                       convert_unicode=True,
                       # pool_recycle=app.config['DB_POOL_RECYCLE'],
                       # pool_size=app.config['DB_POOL_SIZE'],
                       echo=app.config['DB_ECHO'],
                       pool_pre_ping=True)

# SQLAlchemy session
session_maker = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = session_maker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
