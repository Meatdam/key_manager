from authentication import auth_routers
from database.db import AsyncSessionLocal, create_tables
from cipher import cipher_routers
from fastapi import FastAPI

from users import user_routers

app = FastAPI(title="key_manager", version="0.1.0")

app.include_router(user_routers.router)
app.include_router(cipher_routers.router)
app.include_router(auth_routers.router)


@app.on_event('startup')
async def startup_event():
    """
    Подключается к базе данных и создает таблицы при запуске приложения.
    """
    await create_tables()


@app.on_event('shutdown')
async def shutdown_event():
    """
    Закрывает соединение с базой данных при завершении работы приложения.
    """
    await AsyncSessionLocal.close()
