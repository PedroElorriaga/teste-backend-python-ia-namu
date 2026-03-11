from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.database.postgres_setting import Base, engine
from src.modules.users.router import user_router
from src.modules.recommendations.router import recommendation_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router.router)
app.include_router(recommendation_router.router)
