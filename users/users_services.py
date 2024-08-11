from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


from users.users_models import User
from users.users_schemas import UserUpdateSchema, UserOut, UserCreateSchema


async def create_user(user: UserCreateSchema, db: AsyncSession) -> str:
    from authentication.auth_services import hash_password

    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as error:
        await db.rollback()
        raise HTTPException(status_code=409, detail='Пользователь с таким email уже существует')


async def update_user(user_id: int, current_id: int, user: UserUpdateSchema, db: AsyncSession) -> UserOut:
    """
    Обновляет информации о пользователе.

    :param user_id: Идентификатор пользователя (типа int)
    :param user: объект, содержащий данные о пользователе для обновления (типа UserUpdate)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: обновленный пользователь (типа UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()

    if db_user is None or user_id != current_id:
        raise HTTPException(status_code=404, detail='Пользователь не найден или нет прав для изменения')
    if user.password is not None and user.password != db_user.password:
        db_user.password = hash_password(user.password)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_id(user_id: int, db: AsyncSession) -> UserOut:
    """
    Получает данные о пользователе по его идентификатору.
    :param user_id: идентификатор пользователя (типа int)
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: данные о пользователе (типа UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return db_user


async def get_all_users(db: AsyncSession) -> list[UserOut]:
    """
    Получает всех пользователей из БД.

    :param db: Экземпляр сессии базы данных (типа AsyncSession)
    :return: список всех пользователей (типа list[UserOut])
    """
    user_list = await db.execute(select(User))
    return user_list.scalars().all()


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
    Получает пользователя по email.

    :param email: Email пользователя
    :param db: экземпляр сессии базы данных (типа AsyncSession)
    :return: пользователь с указанным email (типа User)
    """
    email = await db.execute(select(User).filter(User.email == email))
    db_user = email.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return db_user


async def delete_user(user_id: int, curent_id: int,  db: AsyncSession) -> UserOut:
    """
    Удаляет пользователя по идентификатору.

    :param user_id: Идентификатор пользователя (тип int)
    :param db: экземпляр сессии базы данных (тип AsyncSession)
    :return: удаленный пользователь (тип UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()

    if db_user is None or user_id != curent_id:
        raise HTTPException(status_code=404, detail='Пользователь не найден или нет прав для удаления')

    await db.delete(db_user)
    await db.commit()
    return db_user
