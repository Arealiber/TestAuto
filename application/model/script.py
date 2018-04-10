# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from application import engine

Base = declarative_base()


class Script(Base):
    __tablename__ = 'script'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    script_name = Column(String(100), nullable=False, unique=True)
    create_by = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'script_name': self.script_name,
            'create_by': self.create_by,
            'create_time': self.create_time,
            'udpate_time': self.update_time
        }


class ScriptInterfaceRelation(Base):
    __tablename__ = 'script_interface_relation'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    script_id = Column(Integer, nullable=False)
    interface_id = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'script_id': self.script_id,
            'interface_id': self.interface_id,
            'order': self.order,
            'create_time': self.create_time,
            'update_time': self.update_time
        }


Base.metadata.create_all(engine)
