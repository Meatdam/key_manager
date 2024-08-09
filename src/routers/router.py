from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.db import get_db
from src.schemas.schemas import CipherMessageSchema
from src.services.service import create_cipher, get_cipher_list, get_cipher_by_id, decrypt_cipher

router = APIRouter(
    prefix="/api/key",
    tags=["key"],
    responses={404: {"description": "Not Found"}},
)


@router.post('/')
async def create_cipher_message(message: CipherMessageSchema,  db: AsyncSession = Depends(get_db)):
    """
    Создать новое зашифрованное сообщение и сохранение в БД
    """
    cipher_message = await create_cipher(message, db)
    return {'message': 'ok', 'cipher': cipher_message}


@router.get('/{cipher_id}')
async def get_cipher_message(cipher_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить зашифрованное сообщение по его id
    """
    cipher_id = await get_cipher_by_id(cipher_id, db)
    return {'status': 'ok', 'cipher': cipher_id}


@router.get('/')
async def get_key_list(db: AsyncSession = Depends(get_db)):
    """
    Получить список зашифрованных сообщений
    """
    cipher_list = await get_cipher_list(db)
    return {'status': 'ok', 'cipher_list': cipher_list}


@router.get('/api/{cipher_message}')
async def decrypt_cipher_message(cipher_message: str, db: AsyncSession = Depends(get_db)):
    """
    Расшифровать зашифрованное сообщение
    """
    try:
        decrypted_message = await decrypt_cipher(cipher_message, db)
        return {'status': 'ok', 'decrypted_message': decrypted_message}
    except Exception as e:
        return {'message': 'Сообщения больше нет :('}
