import os
from datetime import datetime
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import Integer, Column, String, TIMESTAMP, ForeignKey, Enum as EnumType

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from models.models import user

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


from enum import Enum


class LifeCipher(str, Enum):
    one_hour = '1 час'
    one_day = '1 день'
    seven_days = '7 дней'


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    register_date = Column(TIMESTAMP, default=datetime.utcnow)
    password = Column(String, nullable=False)


class Cipher(Base):
    __tablename__ = 'cipher'
    id = Column(Integer, primary_key=True, index=True)
    cipher_message = Column(String, nullable=False)
    key_cipher = Column(String, nullable=False)
    pass_phrase = Column(String, nullable=True)
    url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(user.c.id))
    life_cipher = Column(EnumType(LifeCipher), nullable=True)
    create_date = Column(TIMESTAMP, default=datetime.utcnow)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield session
