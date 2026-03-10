from fastapi import FastAPI
from src.database.postgres_setting import Base, engine
from src.modules.users.models.user_model import User
from src.modules.users.router import user_router


app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(user_router.router)
