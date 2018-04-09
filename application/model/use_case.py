from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
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
    use_case_name = Column(String(20), nullable=False, unique=True)
    script_id = Column(Integer)
    auto_run = Column(Boolean, default=False, nullable=False)
    desc = Column(String(255))
    create_by = Column(Integer)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'use_case_name': self.use_case_name,
            'script_id': self.script_id,
            'auto_run': self.auto_run,
            'desc': self.desc,
            'create_by': self.create_by,
            'create_time': self.create_time,
            'update_time': self.update_time
        }


Base.metadata.create_all(engine)
