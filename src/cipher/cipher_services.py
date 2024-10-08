from cryptography.fernet import Fernet
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate

from src.models.models import Cipher

from src.cipher.cipher_schemas import CipherMessageSchema


key = Fernet.generate_key()
fernet = Fernet(key)


async def create_cipher(message: CipherMessageSchema, user_id: int, db: AsyncSession):
    """
    Create a new encrypted message and save it to the database.
    """
    messages = message.cipher_message
    cipher_message = fernet.encrypt(messages.encode())
    pass_phrase = message.pass_phrase
    cipher_phrase = fernet.encrypt(pass_phrase.encode())

    load_data = Cipher(key_cipher=str(key), cipher_message=str(cipher_message), pass_phrase=str(cipher_phrase),
                       user_id=user_id, url=f"http://127.0.0.1:8000/api/cipher/secrets/{cipher_message}",
                       life_cipher=message.life_cipher)
    db.add(load_data)
    await db.commit()
    await db.refresh(load_data)
    return load_data


async def get_cipher_list(current_id: int, db: AsyncSession,
                          params: Params = Params()):
    """
    Get list of encrypted messages.
    """
    query = select(Cipher).where(Cipher.user_id == current_id)

    return await paginate(db, query, params)


async def get_cipher_by_id(id_message: int, current_id: int, db: AsyncSession) -> Cipher:
    """
    Get encrypted message by its id.
    """
    query = await db.execute(select(Cipher).where(Cipher.id == id_message))
    db_message = query.scalars().first()
    if db_message is None or id_message != current_id:
        raise HTTPException(status_code=404, detail='Сообщение не найдено, или не хватает прав доступа')
    return db_message


async def decrypt_cipher(url: str, pass_phrase: str, db: AsyncSession):
    """
    Decrypting an encrypted message and deleting it from the database.
    """
    message = await db.execute(select(Cipher).where(Cipher.cipher_message == url))
    db_message = message.scalars().first()

    try:
        pass_phrase_cut = db_message.pass_phrase[2:-1]
        keys_cut = db_message.key_cipher[2:-1]

        phrase_cut_bytes = pass_phrase_cut.encode(encoding='utf-8')
        key_bytes = keys_cut.encode(encoding='utf-8')

        f = Fernet(key_bytes)
        decrypted = f.decrypt(phrase_cut_bytes)
        phrase_encode = decrypted.decode(encoding='utf-8')
    except Exception as error:
        raise HTTPException(status_code=403, detail=f'Ошибка при расшифровке или ссылка не действительна{error}')

    if phrase_encode.lower() == pass_phrase.lower():
        try:
            cipher_message_cut = db_message.cipher_message[2:-1]
            cipher_message_bytes = cipher_message_cut.encode(encoding='utf-8')
            decrypted_cipher_message = f.decrypt(cipher_message_bytes)
            encode_cipher_message = decrypted_cipher_message.decode(encoding='utf-8')
            await db.delete(db_message)
            await db.commit()

            return encode_cipher_message
        except Exception as error:
            return {'message': f'Ошибка при расшифровке{error}'}

    elif phrase_encode.lower() != pass_phrase.lower():
        raise HTTPException(status_code=403, detail='Неверное проверочное слово')
    elif pass_phrase is None:
        raise HTTPException(status_code=403, detail='Укажите проверочное слово')
