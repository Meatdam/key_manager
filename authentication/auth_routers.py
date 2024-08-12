import os
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from database.db import User
from authentication.auth_schemas import TokenSchema, RefreshTokenSchema
from users.users_schemas import UserCreateSchema
from authentication.auth_services import (create_access_token, create_refresh_token, validate_token, get_user,
                                          authenticate_user)

from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.post('/token', response_model=TokenSchema)
async def login_for_access_token(form_data: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Получение JWT токен для доступа к API.
    """
    user = await authenticate_user(get_user, form_data.email, form_data.password, db)
    if not user or not isinstance(user, User):
        raise HTTPException(
            status_code=401,
            detail="Проверьте введенные данные пользователя и пароля.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=float(os.getenv('MINUTES')))
    access_token = create_access_token(data={'sub': user.email, 'fresh': True}, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(minutes=float(os.getenv('REFRESH_MINUTES')))
    refresh_token_result = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_result,
    }


@router.post('/refresh_token', response_model=TokenSchema)
async def refresh_token(form_data: RefreshTokenSchema, db: AsyncSession = Depends(get_db)):
    """
    Обновляет JWT токен при помощи refresh токена.
    """
    user = await validate_token(db, token=form_data.refresh_token)

    access_token_expires = timedelta(minutes=float(os.getenv('MINUTES')))
    access_token = create_access_token(data={"sub": user.email, "fresh": False}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(minutes=float(os.getenv('REFRESH_MINUTES')))
    refresh_token_result = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_result,
    }
