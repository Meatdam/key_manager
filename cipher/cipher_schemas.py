from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from database.db import LifeCipher


class CipherMessageSchema(BaseModel):
    """
    Схема для зашифрованного сообщения
    """
    cipher_message: str
    pass_phrase: str
    life_cipher: Optional[LifeCipher] = Field(None)


class EncodingSchema(BaseModel):
    """
    Схема для зашифрованного сообщения с ключом
    """
    pass_phrase: str

    @property
    def encoding_key(self):
        if self.pass_phrase is None:
            raise HTTPException(status_code=403, detail='Укажите проверочное слово')


class CipherOutput(BaseModel):
    """
    Схема для ответа с зашифрованным сообщением
    """
    cipher_message: str
    pass_phrase: str
    key_cipher: str
    url: str

    class Config:
        """
        Конфигурационный класс для настройки ORM.
        Позволяет использовать ORM-объекты для сериализации.
        """
        orm_mode = True


class MessageOutSchema(BaseModel):
    """
    Схема для ответа с зашифрованным сообщением и полями id, email и password.
    """
    cipher_message: str
    pass_phrase: str
    key_cipher: str

    class Config:
        """
        Конфигурационный класс для настройки ORM.
        Позволяет использовать ORM-объекты для сериализации.
        """
        orm_mode = True
