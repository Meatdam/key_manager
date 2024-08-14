from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params

from src.base.responses import ResponseSchema
from src.users import users_services as crud

from src.database.db import get_db
from src.authentication.auth_services import get_current_user
from src.models.models import User

from src.users.users_schemas import UserCreateSchema, UserOut, UserUpdateSchema
from src.users.users_services import create_user, get_user_by_email

router = APIRouter()

responses = ResponseSchema()


@router.post(
    '/create/',
    response_model=UserOut,
    responses=responses()
)
async def add_user(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Adds a new user to the database.

    :param user: An object containing data about the new user (of type UserCreate)
    :param db: An instance of the database session (of type AsyncSession)
    :return: The added user (of type UserOut)
    """
    return await create_user(user, db)


@router.put(
    '/update/{user_id}',
    response_model=UserOut,
    responses=responses()
)
async def update_user(user_id: int, user: UserUpdateSchema, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Gets data about a user by their ID.
    """
    return await crud.update_user(user_id, current_user.id, user, db)


@router.get(
    '/{user_id}',
    response_model=UserOut,
    responses=responses()
)
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Gets data about a user by their ID.
    """
    return await crud.get_user_id(user_id, db)


@router.get(
    '/email/{email}',
    response_model=UserOut,
    responses=responses()
)
async def user_by_email(email: str, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """
    Receives user data via email.
    """
    return await get_user_by_email(email, db)


@router.get(
    '/users',
    response_model=Page[UserOut],
    responses=responses(),
)
async def get_all_users(db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user),
                        page: int = Query(1, gt=0), size: int = Query(50, gt=0)):
    """
    Gets all users from the database.
    """
    params = Params(page=page, size=size)
    return await crud.get_all_users(db, params)


@router.delete(
    '/delete/{user_id}',
    response_model=UserOut,
    responses=responses()
)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Removes a user from the database by its ID.
    """

    return await crud.delete_user(user_id, current_user.id, db)
