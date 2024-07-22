from fastapi import FastAPI

from app.database import Base, engine
from app.routers import user, post, comment
from app.models.user import DBUser
from app.models.post import DBPost
from app.models.comment import DBComment

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(comment.router, prefix="/comments", tags=["comments"])
