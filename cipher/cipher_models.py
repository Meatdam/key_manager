from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from database.db import Base


class MessageCipher(Base):
    """
    Класс для хранения зашифрованных сообщений в БД
    """
    __tablename__ = 'message_cipher'
    id = Column(Integer, primary_key=True, index=True)
    cipher_message = Column(String, nullable=False)
    key_cipher = Column(String, nullable=False)
    pass_phrase = Column(String, nullable=False)
    url = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="messages")
