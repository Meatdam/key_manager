import asyncio
from datetime import datetime, timedelta

from celery import shared_task
from sqlalchemy import select

from database.db import Cipher, LifeCipher, async_session_maker


async def task_to_delete():
    """
    Задача для удаления зашифрованных кодов с истечением срока
    """
    async with async_session_maker() as session:

        hour = await session.execute(select(Cipher).where(Cipher.life_cipher == LifeCipher.one_hour).
                                     where(Cipher.create_date + timedelta(minutes=1) < datetime.now()))
        day = await session.execute(select(Cipher).where(Cipher.life_cipher == LifeCipher.one_day).
                                    where(Cipher.create_date + timedelta(days=1) < datetime.now()))
        seven = await session.execute(select(Cipher).where(Cipher.life_cipher == LifeCipher.seven_days).
                                      where(Cipher.create_date + timedelta(days=7) < datetime.now()))
        time_none = await session.execute(select(Cipher).where(Cipher.create_date + timedelta(days=7) < datetime.now()))

        hour_delete = hour.scalars().all()
        day_delete = day.scalars().all()
        seven_delete = seven.scalars().all()
        time_none_delete = time_none.scalars().all()
        result_time = []
        result_time.extend(hour_delete)
        result_time.extend(day_delete)
        result_time.extend(seven_delete)
        result_time.extend(time_none_delete)
        for i in result_time:
            await session.delete(i)
        await session.commit()


@shared_task
def delete_cipher():
    """
    Периодическая задача для удаления зашифрованных кодов с истечением срока
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task_to_delete())
