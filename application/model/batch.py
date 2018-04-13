from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from application import engine

Base = declarative_base()


class Batch(Base):
    __tablename__ = 'batch'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    batch_name = Column(String(100), nullable=False, unique=True)
    create_by = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'batch_name': self.batch_name,
            'create_by': self.create_by,
            'create_time': self.create_time,
            'update_time': self.update_time
        }


class BatchUseCaseRelation(Base):
    __tablename__ = 'batch_use_case_relation'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, nullable=False)
    use_case_id = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'batch_id': self.batch_id,
            'use_case_id': self.use_case_id,
            'create_time': self.create_time,
            'update_time': self.update_time
        }


Base.metadata.create_all(engine)