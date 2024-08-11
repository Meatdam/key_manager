import os
from datetime import timedelta, datetime
from typing import Callable, Union
from passlib.context import CryptContext
from sqlalchemy import select

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from users.users_models import User
from users import users_services as crud

load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Создает JWT токен с указанными данными и временем жизни.
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=float(os.getenv('MINUTES')))
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
        return encoded_jwt
    except Exception as error:
        raise HTTPException(status_code=500, detail='Ошибка при создании токена')


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Создает JWT токен для refresh с указанными данными и временем жизни.
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
        return encoded_jwt
    except Exception as error:
        raise HTTPException(status_code=500, detail='Ошибка при создании токена')


def verify_password(plain_password, hashed_password) -> bool:
    """
    Верифицирует пароль с зашифрованным паролем.
    """
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(get_user: Callable, email: str, password: str, db: AsyncSession) -> Union[User, bool]:
    """
    Аутентификация пользователя по предоставленным электронной почте и паролю.
    """
    user = await get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """
    Получает текущего пользователя на основе предоставленного JWT токена.

    """
    exception = HTTPException(
        status_code=401,
        detail='Не удалось подтвердить подлинность токена',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        decoded_jwt = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        email = decoded_jwt.get('sub')
        if email is None:
            raise exception
    except jwt.PyJWTError:
        raise exception
    user = await crud.get_user_by_email(email, db)
    if user is None:
        raise exception
    return user


async def get_user(email: str, db: AsyncSession) -> User:
    """
    Получает пользователя по электронной почте.

    """
    query = await db.execute(select(User).filter(User.email == email))
    user = query.scalars().first()
    return user


async def validate_token(db: AsyncSession, token: str = Depends(oauth2_scheme)):
    """
    Валидатор JWT токен и возвращает текущего пользователя.
    """
    user = await get_current_user(db, token=token)
    return user


def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием алгоритма bcrypt.
    """
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.hash(password)
