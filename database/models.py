from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String(100))
    age = Column(Integer)
    birth_date = Column(Date)
    zodiac = Column(String(50))
    registration_date = Column(Date)
