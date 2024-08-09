from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship

from src.config.db import Base


class KeyCipher(Base):
    """
    Класс для хранения ключей шифрования в БД
    """
    __tablename__ = 'key_cipher'
    id = Column(Integer, primary_key=True, index=True)
    cipher_key = Column(VARCHAR(500))
    url = Column(VARCHAR(500))

    message_cipher_id = Column(Integer, ForeignKey("message_cipher.id"))
    message_cipher = relationship("MessageCipher", back_populates="key_cipher")






