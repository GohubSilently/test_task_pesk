from fastapi import APIRouter
from app.api.endpoints import auth_router, content_router


main_router = APIRouter()


main_router.include_router(
    auth_router,
    prefix='/auth',
    tags=['Auth']
)
main_router.include_router(
    content_router,
    prefix='/content',
    tags=['Content']
)
