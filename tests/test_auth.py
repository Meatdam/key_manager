
from httpx import AsyncClient

from src.models.models import User


async def test_login_user(async_client: AsyncClient, test_user: User):
    """
    Tests authorization of a new user.

    :param async_client: asynchronous client for making HTTP requests.
    :param test_user: test user.
    """
    user_data = {'email': 'test_email@example.com', 'password': '11111111'}
    response = await async_client.post('/api/user/create/', json=user_data)
    assert response.status_code == 200, 'The user was not added.'
    token_response = await async_client.post('/api/auth/token', json={'email': 'test_email@example.com',
                                                                      'password': '11111111'})
    assert token_response.status_code == 200, 'Failed to get token'


async def test_refresh_token(async_client: AsyncClient, test_user: User):
    """
    Tests user authorization using a refresh token.
    :param async_client: asynchronous client for making HTTP requests.
    :param test_user: test user.
    """
    user_data = {'email': 'test_email@example.com', 'password': '11111111'}
    response = await async_client.post('/api/user/create/', json=user_data)
    assert response.status_code == 200, 'The user was not added.'
    access_token_response = await async_client.post('/api/auth/token', json={'email': 'test_email@example.com',
                                                                             'password': '11111111'})
    assert access_token_response.status_code == 200, 'Failed to get token'

    token = access_token_response.json().get('access_token')

    refresh_token_response = await async_client.post('/api/auth/token/refresh', json={'refresh_token': token})
    assert refresh_token_response.status_code == 200, 'Failed to get token'
