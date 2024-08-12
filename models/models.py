from datetime import datetime


from sqlalchemy import Column, Table, Integer, String, TIMESTAMP, ForeignKey, Enum as EnumType

from sqlalchemy import MetaData


metadata = MetaData()

from enum import Enum


class LifeCipher(str, Enum):
    one_hour = '1 час'
    one_day = '1 день'
    seven_days = '7 дней'


user = Table(
    'user',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("register_date", TIMESTAMP, default=datetime.utcnow),
)


cipher = Table(
    'cipher',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("cipher_message", String, nullable=False),
    Column("key_cipher", String, nullable=False),
    Column("pass_phrase", String, nullable=False),
    Column("create_date", TIMESTAMP, default=datetime.utcnow),
    Column("life_cipher", EnumType(LifeCipher), nullable=True),  # Enum('1 час', '1 день', '7 дней')
    Column("url", String, nullable=False),
    Column("user_id", Integer, ForeignKey(user.c.id)),
)
