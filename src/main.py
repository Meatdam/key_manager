import typing

import uvicorn

from src.authentication import auth_routers
from src.cipher import cipher_routers
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.users import user_routers

_Message = typing.Dict[str, typing.Any]
_Receive = typing.Callable[[], typing.Awaitable[_Message]]
_Send = typing.Callable[
    [typing.Dict[str, typing.Any]], typing.Coroutine[None, None, None]
]
_ASGIApp = typing.Callable[
    [typing.Dict[str, typing.Any], _Receive, _Send], typing.Coroutine[None, None, None]
]
AppType = typing.TypeVar('AppType', bound='Starlette')

app: _ASGIApp | AppType = FastAPI(title='key_manager', docs_url='/api/docs/', redoc_url='/api/redoc')

add_pagination(app)

app.include_router(user_routers.router, prefix='/api/user', tags=['User'])
app.include_router(cipher_routers.router, prefix='/api/cipher', tags=['Cipher'])
app.include_router(auth_routers.router, prefix='/api/auth', tags=['Auth'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
