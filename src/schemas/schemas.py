from pydantic import BaseModel


class CipherSchema(BaseModel):
    cipher_message: str
