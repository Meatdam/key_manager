from src.config.db import AsyncSessionLocal, create_tables
from src.routers.router import router as filter_router
from fastapi import FastAPI


app = FastAPI()

app.include_router(filter_router)


@app.on_event('startup')
async def startup_event() -> None:
    """
    Подключается к базе данных и создает таблицы при запуске приложения.
    """
    await create_tables()


@app.on_event('shutdown')
async def shutdown_event() -> None:
    """
    Закрывает соединение с базой данных при завершении работы приложения.
    """
    await AsyncSessionLocal.close()
