from fastapi import FastAPI

from app.database import Base, engine
from app.routers import user
from app.models.user import DBUser
from app.models.post import DBPost
from app.models.comment import DBComment

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/users", tags=["users"])
