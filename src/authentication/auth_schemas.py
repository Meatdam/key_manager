from pydantic import BaseModel


class TokenSchema(BaseModel):
    """
    Model for describing JWT tokens.
    """
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


class RefreshTokenSchema(BaseModel):
    """
    Model for describing JWT tokens for refresh tokens.
    """
    refresh_token: str
