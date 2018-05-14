from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from application import engine

Base = declarative_base()


class EnvironmentLine(Base):
    __tablename__ = 'environment_line'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True)
    environment_name = Column(String(100), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'environment_name': self.environment_name,
        }


class EnvironmentInfo(Base):
    __tablename__ = 'environment_line_info'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True)
    environment_id = Column(Integer, primary_key=True)
    url = Column(String(100), nullable=False)
    map_ip = Column(String(100), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'environment_id': self.environment_id,
            'url': self.url,
            'map_ip': self.map_ip,
        }


Base.metadata.create_all(engine)
