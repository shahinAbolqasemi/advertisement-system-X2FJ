from fastapi import FastAPI, status
from starlette.middleware.cors import CORSMiddleware

from . import database
from .middlewares import AuthenticationMiddleware, BearerTokenAuthBackend
from .routers.ad import router as ad_router
from .routers.auth import router as auth_router

database.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    AuthenticationMiddleware,
    backend=BearerTokenAuthBackend()
)


@app.get('/ping', status_code=status.HTTP_200_OK)
async def ping():
    return {'message': 'pong'}


app.include_router(auth_router, prefix='/auth')
app.include_router(ad_router, prefix='/ad')
