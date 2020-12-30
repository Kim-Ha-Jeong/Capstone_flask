from sqlalchemy import *
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.email)


class Full(Base):
    __tablename__ = 'full'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    size = Column(String(20))
    storage_path = Column(String(50))
