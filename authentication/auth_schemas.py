from pydantic import BaseModel


class TokenSchema(BaseModel):
    """
    Модель для описания JWT токенов.
    """
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


class RefreshTokenSchema(BaseModel):
    """
    Модель для описания JWT токенов для refresh токенов.
    """
    refresh_token: str
