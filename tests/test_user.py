
from httpx import AsyncClient
from starlette import status

from src.models.models import User
from tests.conftest import create_test_auth_headers_for_user


async def test_add_user(async_client: AsyncClient):
    """
    Tests creating a new user.

    :param async_client: asynchronous client for making HTTP requests
    :return:
    """
    user_data = {'email': 'test_email@example.com', 'password': 'password'}
    response = await async_client.post('/api/user/create/', json=user_data)
    data_from_response = response.json()
    assert response.status_code == 200, 'Пользователь не был добавлен'
    assert data_from_response.get('email') == user_data.get('email')


async def test_add_user_duplicate_email_error(async_client: AsyncClient):
    """
    Tests creating a user with the same email
    :param async_client: asynchronous client for making HTTP requests
    :return:
    """
    user_data = {'email': 'test_email@example.com', 'password': 'password'}
    user_data_same = {'email': 'test_email@example.com', 'password': 'password'}
    response = await async_client.post('/api/user/create/', json=user_data)
    assert response.status_code == 200, 'The user was not added.'
    response = await async_client.post('/api/user/create', json=user_data_same)
    assert response.status_code == 405, "You can't add two users with the same email."


async def test_get_user(async_client: AsyncClient, test_user: User):
    """
    Tests getting a user by their id.

    :param async_client: asynchronous client for making HTTP requests
    :param test_user: test user
    :return:
    """
    response = await async_client.get(f'/api/user/{test_user.id}',
                                      headers=create_test_auth_headers_for_user(test_user.email))
    assert response.status_code == 200


async def test_get_users(async_client: AsyncClient, test_user: User):
    """
    Tests getting a list of users.

    :param async_client: asynchronous client for making HTTP requests
    :param test_user: test user
    :return:
    """
    response = await async_client.get('/api/user/users', headers=create_test_auth_headers_for_user(test_user.email),
                                      params={'page': 1, 'size': 50})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_update_user(async_client: AsyncClient, test_user: User):
    """
    Tests user change.

    :param async_client: asynchronous client for making HTTP requests
    :param test_user: test user
    :return:
    """
    user_data_updated = {'email': test_user.email, 'password': '333099393'}
    response = await async_client.put(f'/api/user/update/{test_user.id}',
                                      headers=create_test_auth_headers_for_user(test_user.email),
                                      json=user_data_updated)
    assert response.status_code == 200


async def test_delete_user(async_client: AsyncClient, test_user: User):
    """
    Tests deleting a user.

    :param async_client: asynchronous client for making HTTP requests
    :param test_user: test user
    :return:
    """
    response = await async_client.delete(f'/api/user/delete/{test_user.id}',
                                         headers=create_test_auth_headers_for_user(test_user.email))
    assert response.status_code == 200
