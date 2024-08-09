from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from src.config.db import Base


class MessageCipher(Base):
    """
    Класс для хранения зашифрованных сообщений в БД
    """
    __tablename__ = 'message_cipher'
    id = Column(Integer, primary_key=True, index=True)
    cipher_message = Column(VARCHAR(500))

    key_cipher = relationship('KeyCipher', back_populates='message_cipher')
