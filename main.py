from authentication import auth_routers
from cipher import cipher_routers
from fastapi import FastAPI

from users import user_routers

app = FastAPI(title="key_manager", version="0.1.0")

app.include_router(user_routers.router)
app.include_router(cipher_routers.router)
app.include_router(auth_routers.router)
