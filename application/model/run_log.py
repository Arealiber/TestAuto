# -*- coding:utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

from application import engine

Base = declarative_base()


class TestCaseRunLog(Base):
    __tablename__ = 'test_case_run_log'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    test_case_name = Column(String(100), nullable=False)
    is_pass = Column(Boolean, nullable=False)
    run_time = Column(DateTime, default=datetime.utcnow)
    cost_time = Column(Integer, default=0, nullable=False)
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return{
            'id': self.id,
            'test_case_name': self.test_case_name,
            'is_pass': self.is_pass,
            'run_time': self.run_time
        }


class RelationInterfaceRunLog(Base):
    __tablename__ = "relation_interface_run_log"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf-8"
    }

    id = Column(Integer, primary_key=True)
    relation_id = Column(Integer, nullable=False)  # 关联的testcase运行的日志id
    interface_name = Column(String(100), nullable=False)
    run_res = Column(String(1000), nullable=False)
    run_time = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'relation_id': self.relation_id,
            'interface_name': self.interface_name,
            'run_res': self.run_res,
            'run_time': self.run_time
        }


Base.metadata.create_all(engine)

