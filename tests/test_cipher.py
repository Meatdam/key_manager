
from httpx import AsyncClient

from src.models.models import User
from tests.conftest import create_test_auth_headers_for_user


async def test_generate_cipher(async_client: AsyncClient, test_user: User):
    """
    Tests creating a new secret.

    :param async_client: asynchronous client for making HTTP requests
    :param test_user: test user
    :return:
    """
    secret_data = {'life_cipher': '1 час', 'cipher_message': 'cipher_message', 'pass_phrase': 'passphrase'}
    response = await async_client.post(
        '/api/cipher/generate',
        headers=create_test_auth_headers_for_user(test_user.email),
        json=secret_data)

    assert response.status_code == 200, 'The secret was not added.'


async def test_get_secret(async_client: AsyncClient, test_user: User):
    """
    Tests getting a secret by its key.

    :param async_client: asynchronous client for making HTTP requests
    :param test_user: test user
    :return:
    """
    secret_data = {'life_cipher': '1 час', 'cipher_message': 'cipher_message', 'pass_phrase': 'passphrase'}
    response = await async_client.post(
        '/api/cipher/generate',
        headers=create_test_auth_headers_for_user(test_user.email),
        json=secret_data)
    cipher_message = response.json().get('cipher_message')

    assert response.status_code == 200
    assert cipher_message is not None
