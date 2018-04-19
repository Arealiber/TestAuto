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
    use_case_name = Column(String(100), nullable=False)
    is_pass = Column(Boolean, nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)
    run_time = Column(Float, default=0, nullable=False)
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return{
            'id': self.id,
            'use_case_id': self.use_case_id,
            'is_pass': self.is_pass,
            'create_time': self.create_time,
            'run_time': self.run_time
        }


class RelationInterfaceRunLog(Base):
    __tablename__ = "relation_interface_run_log"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf-8"
    }

    id = Column(Integer, primary_key=True)
    use_case_run_log_id = Column(Integer, nullable=False)  # 关联的testcase运行的日志id
    interface_id = Column(Integer, nullable=False)
    res_status_code = Column(Integer, nullable=False)
    res_headers = Column(String(1000), nullable=False)
    res_payload = Column(String(10000), nullable=False)
    is_pass = Column(Boolean, nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'use_case_run_log_id': self.use_case_run_log_id,
            'interface_id': self.interface_id,
            'res_status_code': self.res_status_code,
            'res_headers': self.res_headers,
            'res_payload': self.res_payload,
            'is_pass': self.is_pass
        }


Base.metadata.create_all(engine)

