from fastapi import FastAPI, status
from starlette.middleware.cors import CORSMiddleware

from app.routers.ad import router as ad_router
from app.routers.auth import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/ping', status_code=status.HTTP_200_OK)
async def ping():
    return {'message': 'pong'}


app.add_route('auth/', auth_router, name='authentication')
app.add_route('ad/', ad_router, name='advertisement')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('app.main:app')
