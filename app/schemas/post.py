from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.comment import Comment


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    is_blocked: bool
    owner_id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True
