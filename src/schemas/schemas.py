from pydantic import BaseModel


class CipherMessageSchema(BaseModel):
    """
    Схема для зашифрованного сообщения
    """
    cipher_message: str


class KeyCipherSchema(BaseModel):
    """
    Схема для ключа шифрования
    """
    cipher_key: str
    url: str
