
import asyncio
import uuid
from datetime import timedelta
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from src.authentication.auth_services import create_access_token
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, TEST_DB_NAME, \
    ACCESS_TOKEN_EXPIRE_MINUTES
from src.database.db import get_db, Base
from src.main import app
from src.models.models import User

DATABASE_URL_TEST = (f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@'
                     f'{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}')

engine_test = create_async_engine(DATABASE_URL_TEST)
AsyncSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Creates and returns a test database session instance.
    """
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True, scope='function')
async def prepare_database() -> None:
    """
    Connects to the test database and creates tables defined in models inheriting from the Base class.
    Cleans up the database after tests.
    :return:
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Creates and returns an asynchronous client for testing the API.
    :return:
    """
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url='http://test') as a_client:
        yield a_client


@pytest.fixture(scope='session')
def event_loop() -> AsyncGenerator[asyncio.AbstractEventLoop, None]:
    """
    Creates and returns a new event loop for testing.
    :return:
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def test_user() -> AsyncGenerator[User, None]:
    """
    Creates and returns a test user.
    :return:
    """
    unique_email = f'test_email_{uuid.uuid4()}@example.com'
    user = User(email=unique_email, password='test_password')
    async with AsyncSessionLocal() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    yield user


def create_test_auth_headers_for_user(email: str) -> dict[str, str]:
    """
    Creates authorization headers for a user given their email.

    :param email: user's email (type str)
    :return: authorization headers (type dict)
    """
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES)),
    )
    return {"Authorization": f"Bearer {access_token}"}
