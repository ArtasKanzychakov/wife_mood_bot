from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User
from config.settings import Config
from datetime import datetime  # Добавлен импорт

engine = create_engine(Config.POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_user(db, telegram_id: int, name: str, age: int, birth_date, zodiac: str):
    user = User(
        telegram_id=telegram_id,
        name=name,
        age=age,
        birth_date=birth_date,
        zodiac=zodiac,  # Убрана несуществующая функция zinc()
        registration_date=datetime.now()
    )
    db.add(user)
    db.commit()
    return user
