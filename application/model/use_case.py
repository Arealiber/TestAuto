# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

from application import engine

Base = declarative_base()


class UseCase(Base):
    __tablename__ = 'use_case'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    use_case_name = Column(String(100), nullable=False)
    auto_run = Column(Boolean, nullable=False, default=False)
    desc = Column(String(1000))
    create_by = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'use_case_name': self.use_case_name,
            'auto_run': self.auto_run,
            'desc': self.desc,
            'create_by': self.create_by,
            'create_time': self.create_time,
            'update_time': self.update_time
        }


class UseCaseInterfaceRelation(Base):
    __tablename__ = 'use_case_interface_relation'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    use_case_id = Column(Integer, nullable=False)
    interface_id = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    eval_string = Column(String(1000))
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'use_case_id': self.use_case_id,
            'interface_id': self.interface_id,
            'order': self.order,
            'eval_string': self.eval_string,
            'create_time': self.create_time,
            'update_time': self.update_time
        }


class UseCaseParameterRelation(Base):
    __tablename__ = 'use_case_parameter_relation'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    relation_id = Column(Integer, nullable=False)
    parameter_name = Column(String(20), nullable=False)
    parameter_value = Column(String(200))
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'relation_id': self.relation_id,
            'parameter_name': self.parameter_name,
            'parameter_value': self.parameter_value,
            'create_time': self.create_time,
            'update_time': self.update_time
        }


Base.metadata.create_all(engine)
