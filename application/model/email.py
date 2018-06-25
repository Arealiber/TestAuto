from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

from application import engine

Base = declarative_base()


class Email(Base):
    __tablename__ = 'batch'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    email_account = Column(String(50), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email_account': self.email_account,
            'create_time': self.create_time
        }


Base.metadata.create_all(engine)
