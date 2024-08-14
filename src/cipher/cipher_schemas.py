from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from src.models.models import LifeCipher


class CipherMessageSchema(BaseModel):
    """
    Scheme for encrypted message
    """
    cipher_message: str
    pass_phrase: str
    life_cipher: Optional[LifeCipher] = Field(None)


class EncodingSchema(BaseModel):
    """
    Scheme for encrypted message with key
    """
    pass_phrase: str

    @property
    def encoding_key(self):
        if self.pass_phrase is None:
            raise HTTPException(status_code=403, detail='Укажите проверочное слово')


class CipherOutput(BaseModel):
    """
    Scheme for replying with encrypted message
    """
    cipher_message: str
    pass_phrase: str
    key_cipher: str
    url: str

    class Config:
        """
        Configuration class for ORM setup.
        Allows using ORM objects for serialization.
        """
        orm_mode = True


class MessageOutSchema(BaseModel):
    """
    Schema for a response with an encrypted message and id, email and password fields.
    """
    cipher_message: str
    pass_phrase: str
    key_cipher: str
    url: str
    id: int

    class Config:
        """
        Configuration class for ORM setup.
        Allows using ORM objects for serialization.
        """
        orm_mode = True
