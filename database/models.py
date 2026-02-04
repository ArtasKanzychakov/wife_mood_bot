from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    zodiac = Column(String(20))
    notify_enabled = Column(Boolean, default=True)
    timezone = Column(String(50), default='Europe/Moscow')
    created_at = Column(DateTime, default=datetime.now)
    last_active = Column(DateTime, default=datetime.now)


class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    content_type = Column(String(50))  # horoscope, news, quote
    content_id = Column(String(255))
    content_text = Column(String(1000))
    created_at = Column(DateTime, default=datetime.now)