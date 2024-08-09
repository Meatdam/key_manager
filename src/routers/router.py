from fastapi import APIRouter

from src.schemas.schemas import CipherSchema
from src.services.service import create_cipher, get_cipher_list, get_cipher_by_id, decrypt_cipher

router = APIRouter(
    prefix="/api/key",
    tags=["key"],
    responses={404: {"description": "Not Found"}},
)


@router.post('/')
async def create_cipher_message(key_cipher: CipherSchema):
    """
    Создать новое зашифрованное сообщение и сохранение в БД
    """
    cipher_message = await create_cipher(key_cipher)
    return {'message': 'ok', 'cipher': cipher_message}


@router.get('/{cipher_id}')
async def get_cipher_message(cipher_id: int):
    """
    Получить зашифрованное сообщение по его id
    """
    cipher_id = await get_cipher_by_id(cipher_id)
    return {'status': 'ok', 'cipher': cipher_id}


@router.get('/')
async def get_key_list():
    """
    Получить список зашифрованных сообщений
    """
    cipher_list = await get_cipher_list()
    return {'status': 'ok', 'cipher_list': cipher_list}


@router.get('/api/{cipher_message}')
async def decrypt_cipher_message(cipher_message: str):
    """
    Расшифровать зашифрованное сообщение
    """
    decrypted_message = await decrypt_cipher(cipher_message)
    return {'status': 'ok', 'decrypted_message': decrypted_message}
