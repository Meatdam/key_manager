from cryptography.fernet import Fernet
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.models.key_cipher import KeyCipher
from src.models.message_cipher import MessageCipher
from src.schemas.schemas import CipherMessageSchema

key = Fernet.generate_key()
fernet = Fernet(key)


async def create_cipher(message: CipherMessageSchema, db: AsyncSession) -> str:
    """
    Создание нового зашифрованного сообщения и сохранение в БД
    """
    result = message.cipher_message
    cipher_message = fernet.encrypt(result.encode())
    result_cipher = MessageCipher(cipher_message=str(cipher_message))
    db.add(result_cipher)
    await db.commit()
    await db.refresh(result_cipher)
    cipher_key = KeyCipher(cipher_key=str(key), url=f"http://127.0.0.1:8000/api/key/api/{cipher_message}",
                           message_cipher_id=result_cipher.__dict__.get('id'))
    db.add(cipher_key)
    await db.commit()
    await db.refresh(cipher_key)
    return cipher_key.url


async def get_cipher_list(db: AsyncSession):
    """
    Получить список зашифрованных сообщений
    """
    cipher_list = await db.execute(select(MessageCipher))
    return cipher_list.scalars().all()


async def get_cipher_by_id(id_message: int, db: AsyncSession) -> MessageCipher:
    """
    Получить зашифрованное сообщение по его id
    """
    query = await db.execute(select(MessageCipher).where(MessageCipher.id == id_message))
    db_message = query.scalars().first()
    if db_message is None:
        raise HTTPException(status_code=404, detail='Сообщение не найдено')
    return db_message


async def decrypt_cipher(cipher_message: str, db: AsyncSession) -> str:
    """
    Расшифровка зашифрованного сообщения и удаление из БД
    """

    message = await db.execute(select(MessageCipher).where(MessageCipher.cipher_message == cipher_message))
    db_message = message.scalars().first()

    load_key = await db.execute(select(KeyCipher).where(KeyCipher.message_cipher_id == db_message.__dict__.get('id')))
    db_key = load_key.scalars().first()

    cut_key = db_key.__dict__.get('cipher_key')[2:-1]
    cut_message = db_message.__dict__.get('cipher_message')[2:-1]
    key_bytes = cut_key.encode(encoding='utf-8')
    message_bytes = cut_message.encode(encoding='utf-8')

    f = Fernet(key_bytes)
    decrypted = f.decrypt(message_bytes)
    decrypted_message = decrypted.decode(encoding='utf-8')

    delete_key = await db.execute(select(KeyCipher).where(KeyCipher.message_cipher_id == db_message.__dict__.get('id')))
    db_key = delete_key.scalars().first()
    if db_key is None:
        raise HTTPException(status_code=404, detail='Ключ не найден')
    await db.delete(db_key)
    await db.commit()
    delete_message = await db.execute(select(MessageCipher).where(MessageCipher.cipher_message == cipher_message))
    db_message = delete_message.scalars().first()
    if db_message is None:
        raise HTTPException(status_code=404, detail='Сообщение не найдено')
    await db.delete(db_message)
    await db.commit()
    return decrypted_message
