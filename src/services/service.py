from cryptography.fernet import Fernet

from src.models.models import KeyCipher, UserCipher

key = Fernet.generate_key()
fernet = Fernet(key)


async def create_cipher(message):
    """
    Создание нового зашифрованного сообщения и сохранение в БД
    """
    result = message.cipher_message
    cipher_message = fernet.encrypt(result.encode())
    result_cipher = await KeyCipher.create(cipher_message=cipher_message)
    key_cipher = await UserCipher.create(cipher_key=key, key_cipher_id=result_cipher,
                                         url=f"http://127.0.0.1:8000/api/key/api/{cipher_message}")
    return key_cipher.url


async def get_cipher_list():
    """
    Получить список зашифрованных сообщений
    """
    cipher_list = await KeyCipher.all()
    return cipher_list


async def get_cipher_by_id(id_message):
    """
    Получить зашифрованное сообщение по его id
    :param id_message:
    :return:
    """
    cipher = await KeyCipher.get_or_none(id=id_message)
    return cipher


async def decrypt_cipher(cipher_message):
    """
    Расшифровка зашифрованного сообщения и удаление из БД
    """
    message = await KeyCipher.get_or_none(cipher_message=cipher_message)
    load_key = await UserCipher.get_or_none(key_cipher_id=message.id)

    cut_key = load_key.cipher_key[2:-1]
    cut_message = message.cipher_message[2:-1]

    key_bytes = cut_key.encode(encoding='utf-8')
    message_bytes = cut_message.encode(encoding='utf-8')

    f = Fernet(key_bytes)
    decrypted = f.decrypt(message_bytes)
    decrypted_message = decrypted.decode(encoding='utf-8')

    user_cipher = await UserCipher.get(id=message.id)
    await user_cipher.delete()
    message_cipher = await KeyCipher.get(id=message.id)
    await message_cipher.delete()

    return decrypted_message
