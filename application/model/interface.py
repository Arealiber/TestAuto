# -*- coding:utf-8 -*-

from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from application import engine

Base = declarative_base()


class InterfaceEntry(Enum):
    # TODO 填充真实数据
    h5 = 1
    toC = 2

    des = {
        h5: 'HTML5页面',
        toC: 'To C端'
    }


class InterfaceMethod(Enum):
    GET = 1
    POST = 2

    des = {
        GET: 'GET',
        POST: 'POST'
    }


class Interface(Base):
    __tablename__ = 'interface'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    interface_name = Column(String(100), nullable=False)
    interface_entry = Column(Integer, nullable=False)  # 入口
    interface_url = Column(String(255), nullable=False)
    interface_method = Column(Integer, nullable=False)
    interface_header = Column(String(255))
    interface_json_payload = Column(String(1024))
    create_by = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'interface_name': self.interface_name,
            'interface_entry': self.interface_entry,
            'interface_url': self.interface_url,
            'interface_method': self.interface_method,
            'interface_header': self.interface_header,
            'interface_json_payload': self.interface_json_payload,
            'create_by': self.create_by,
            'create_time': self.create_time,
            'update_time': self.update_time
        }


Base.metadata.create_all(engine)