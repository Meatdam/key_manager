from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.models.models import User

from src.users.users_schemas import UserUpdateSchema, UserOut, UserCreateSchema


async def create_user(user: UserCreateSchema, db: AsyncSession) -> str:
    """
    Creates a new user in the database.

    :param user: an object containing data about the new user (of type UserCreate)
    :param db: an instance of the database session (of type AsyncSession)
    """
    from src.authentication.auth_services import hash_password

    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password, )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as error:
        await db.rollback()
        raise HTTPException(status_code=409, detail=f'Пользователь с таким email уже существует {error}')


async def update_user(user_id: int, current_id: int, user: UserUpdateSchema, db: AsyncSession) -> UserOut:
    """
    Updates user information.

    :param user_id: User ID (of type int)
    :param user: object containing user data to update (of type UserUpdate)
    :param db: database session instance (of type AsyncSession)
    :return: updated user (of type UserOut)
    """
    from src.authentication.auth_services import hash_password
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()

    if db_user is None or user_id != current_id:
        raise HTTPException(status_code=404, detail='Пользователь не найден или нет прав для изменения')
    if user.password is not None and user.password != db_user.password:
        db_user.password = hash_password(user.password)

    for var, value in vars(user).items():
        if value is not None:
            setattr(db_user, var, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_id(user_id: int, db: AsyncSession) -> UserOut:
    """
    Gets user data by user ID.

    :param user_id: User ID (of type int)
    :param db: database session instance (of type AsyncSession)
    :return: user data (of type UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return db_user


async def get_all_users(db: AsyncSession, params: Params = Params()) -> Page[UserOut]:
    """
    Gets all users from the DB.

    :param db: Database session instance (of type AsyncSession)
    :return: list of all users (of type list[UserOut])
    """
    query = select(User)

    return await paginate(db, query, params)


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
    Gets a user by email.

    :param email: User's email
    :param db: database session instance (of type AsyncSession)
    :return: user with the specified email (of type User)
    """
    email = await db.execute(select(User).filter(User.email == email))
    db_user = email.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return db_user


async def delete_user(user_id: int, curent_id: int,  db: AsyncSession) -> UserOut:
    """
    Deletes a user by ID.

    :param user_id: User ID (type int)
    :param db: database session instance (type AsyncSession)
    :return: deleted user (type UserOut)
    """
    query = await db.execute(select(User).where(User.id == user_id))
    db_user = query.scalars().first()

    if db_user is None or user_id != curent_id:
        raise HTTPException(status_code=404, detail='Пользователь не найден или нет прав для удаления')

    await db.delete(db_user)
    await db.commit()
    return db_user
