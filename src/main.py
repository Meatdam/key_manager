from src.authentication import auth_routers
from src.cipher import cipher_routers
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.users import user_routers


app = FastAPI(title="key_manager", version="0.1.0")

add_pagination(app)

app.include_router(user_routers.router)
app.include_router(cipher_routers.router)
app.include_router(auth_routers.router)
