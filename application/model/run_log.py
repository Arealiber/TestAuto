# -*- coding:utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from application import engine


Base = declarative_base()


class UseCaseRunLog(Base):
    __tablename__ = 'test_case_run_log'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    run_key = Column(String(100), nullable=False)  # 指定某次触发标志，必须是独一无二的
    use_case_id = Column(Integer, nullable=False)
    is_pass = Column(Boolean, nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)
    run_time = Column(Float, default=0, nullable=False)

    def to_dict(self):
        return{
            'id': self.id,
            'run_key': self.run_key,
            'use_case_id': self.use_case_id,
            'is_pass': self.is_pass,
            'create_time': self.create_time,
            'run_time': self.run_time
        }


class RelationInterfaceRunLog(Base):
    __tablename__ = "relation_interface_run_log"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    run_key = Column(String(100), nullable=False)
    use_case_run_log_id = Column(Integer, nullable=False)  # 关联的testcase运行的日志id
    interface_id = Column(Integer, nullable=False)
    re_code = Column(Integer, nullable=False)
    re_headers = Column(String(1000), nullable=False)
    re_payload = Column(String(10000), nullable=False)
    is_pass = Column(Boolean, nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'run_key': self.run_key,
            'use_case_run_log_id': self.use_case_run_log_id,
            'interface_id': self.interface_id,
            're_code': self.re_code,
            're_headers': self.re_headers,
            're_payload': self.re_payload,
            'is_pass': self.is_pass
        }


Base.metadata.create_all(engine)

