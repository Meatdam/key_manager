from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Params, Page
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.auth_services import get_current_user
from src.database.db import get_db
from src.cipher.cipher_schemas import CipherMessageSchema, CipherOutput, EncodingSchema, MessageOutSchema
from src.models.models import User


from src.cipher.cipher_services import create_cipher, get_cipher_by_id, get_cipher_list, decrypt_cipher
from src.base.responses import ResponseSchema

router = APIRouter()

responses = ResponseSchema()


@router.post(
    '/generate',
    response_model=CipherOutput,
    responses=responses()
)
async def create_cipher_message(message: CipherMessageSchema,  db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(get_current_user)):
    """
    Create a new encrypted message and save it to the DB
    """
    return await create_cipher(message, current_user.id, db)


@router.get(
    '/{cipher_id}',
    response_model=CipherOutput,
    responses=responses()
)
async def get_cipher_message(cipher_id: int, db: AsyncSession = Depends(get_db),
                             current_user: User = Depends(get_current_user)):
    """
    Get encrypted message by its id
    """
    return await get_cipher_by_id(cipher_id, current_user.id, db)


@router.get(
    '/ciphers',
    response_model=Page[MessageOutSchema],
    responses=responses()
            )
async def get_key_list(db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user),
                       page: int = Query(1, gt=0), size: int = Query(50, gt=0)):
    """
    Get list of encrypted messages
    """
    params = Params(page=page, size=size)
    return await get_cipher_list(current_user.id, db, params)


@router.post('/secrets/{secret_key}',
             responses=responses())
async def decrypt_cipher_message(secret_key: str, form_data: EncodingSchema, db: AsyncSession = Depends(get_db)):
    """
    Decrypt encrypted message
    """
    decrypted_message = await decrypt_cipher(secret_key, form_data.pass_phrase, db)
    return {'status': 'ok', 'Ваше сообщение': decrypted_message}
