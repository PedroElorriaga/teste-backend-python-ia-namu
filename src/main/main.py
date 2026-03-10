from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.database.postgres_setting import Base, engine
from src.modules.users.models.user_model import User
from src.modules.users.router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router.router)
