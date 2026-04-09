from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.routers import main_router
from app.core.db import redis
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis.close()


app = FastAPI(title=settings.app_title, description=settings.app_description, lifespan=lifespan)
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app, reload=True)
