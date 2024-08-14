from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreateSchema(BaseModel):
    """
    Схема для создания нового пользователя
    """
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserUpdateSchema(BaseModel):
    """
    Схема для редактирования пользователя
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)


class UserOut(BaseModel):
    """
    Model for displaying users with id, email and password fields.
    """
    id: int
    email: EmailStr

    class Config:
        """
        Configuration class for ORM setup.
        Allows using ORM objects for serialization.
        """
        orm_mode = True
