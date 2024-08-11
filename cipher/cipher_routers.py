from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from authentication.auth_services import get_current_user
from database.db import get_db
from cipher.cipher_schemas import CipherMessageSchema, CipherOutput, EncodingSchema, MessageOutSchema
from users.users_models import User

from cipher.cipher_services import create_cipher, get_cipher_by_id, get_cipher_list, decrypt_cipher

router = APIRouter(
    prefix="",
    tags=["message"],
    responses={404: {"description": "Not Found"}},
)


@router.post('/', response_model=CipherOutput)
async def create_cipher_message(message: CipherMessageSchema,  db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(get_current_user)):
    """
    Создать новое зашифрованное сообщение и сохранение в БД
    """
    return await create_cipher(message, current_user.id, db)


@router.get('/{cipher_id}', response_model=CipherOutput)
async def get_cipher_message(cipher_id: int, db: AsyncSession = Depends(get_db),
                             current_user: User = Depends(get_current_user)):
    """
    Получить зашифрованное сообщение по его id
    """
    return await get_cipher_by_id(cipher_id, current_user.id, db)


@router.get('/', response_model=List[MessageOutSchema])
async def get_key_list(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Получить список зашифрованных сообщений
    """

    cipher_list = await get_cipher_list(current_user.id, db)

    return cipher_list


@router.get('/key/{url}')
async def decrypt_cipher_message(url: str, form_data: EncodingSchema, db: AsyncSession = Depends(get_db)):
    """
    Расшифровать зашифрованное сообщение
    """
    decrypted_message = await decrypt_cipher(url, form_data.pass_phrase, db)
    return {'status': 'ok', 'Ваше сообщение': decrypted_message}
