from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from .models import Base, User, Favorite
from config.settings import Config
from datetime import datetime

# Инициализация БД
engine = create_engine(Config.POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    """Получить сессию БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_or_create_user(db, telegram_id: int, **kwargs):
    """Получить или создать пользователя"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    
    if not user:
        user = User(telegram_id=telegram_id, **kwargs)
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
    
    user.last_active = datetime.now()
    db.commit()
    return user


def update_user(db, telegram_id: int, **kwargs):
    """Обновить данные пользователя"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.commit()
    return user


def add_favorite(db, user_id: int, content_type: str, content_id: str, content_text: str):
    """Добавить в избранное"""
    favorite = Favorite(
        user_id=user_id,
        content_type=content_type,
        content_id=content_id,
        content_text=content_text[:1000]
    )
    db.add(favorite)
    db.commit()
    return favorite


def get_favorites(db, user_id: int, limit=10):
    """Получить избранное пользователя"""
    return db.query(Favorite).filter(
        Favorite.user_id == user_id
    ).order_by(
        Favorite.created_at.desc()
    ).limit(limit).all()


def delete_favorite(db, favorite_id: int):
    """Удалить из избранного"""
    favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if favorite:
        db.delete(favorite)
        db.commit()
        return True
    return False


def get_all_users(db):
    """Получить всех пользователей"""
    return db.query(User).filter(User.notify_enabled == True).all()