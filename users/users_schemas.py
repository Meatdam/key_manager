from pydantic import BaseModel, EmailStr, Field


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
    email: EmailStr
    password: str = Field(None, min_length=8)


class UserOut(BaseModel):
    """
    Модель для вывода пользователей с полями id, email и password.
    """
    id: int
    email: EmailStr

    class Config:
        """
        Конфигурационный класс для настройки ORM.
        Позволяет использовать ORM-объекты для сериализации.
        """
        orm_mode = True
