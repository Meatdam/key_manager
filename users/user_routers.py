from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from users import users_services as crud

from database.db import get_db
from authentication.auth_services import get_current_user
from database.db import User
from users.users_schemas import UserCreateSchema, UserOut, UserUpdateSchema
from users.users_services import create_user, get_user_by_email

router = APIRouter(
    prefix="",
    tags=["user"],
    responses={404: {"description": "Not Found"}},
)


@router.post('/users/', response_model=UserOut)
async def add_user(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Добавляет нового пользователя в базу данных.

    :param user: Объект, содержащий данные о новом пользователе (типа UserCreate)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: добавленный пользователь (типа UserOut)
    """
    return await create_user(user, db)


@router.put('/users/{user_id}', response_model=UserOut)
async def update_user(user_id: int, user: UserUpdateSchema, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Получает данные о пользователе по его идентификатору.
    """
    return await crud.update_user(user_id, current_user.id, user, db)


@router.get('/users/{user_id}', response_model=UserOut)
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Получает данные о пользователе по его идентификатору.
    """
    return await crud.get_user_id(user_id, db)


@router.get('/users/email/{email}', response_model=UserOut)
async def user_by_email(email: str, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """
    Получает данные о пользователе по email.
    """
    return await get_user_by_email(email, db)


@router.get('/users/', response_model=List[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """
    Получает всех пользователей из базы данных.
    """
    return await crud.get_all_users(db)


@router.delete('/users/{user_id}', response_model=UserOut)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Удаляет пользователя из базы данных по его идентификатору.
    """

    return await crud.delete_user(user_id, current_user.id, db)
