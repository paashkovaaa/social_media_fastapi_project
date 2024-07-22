from typing import List

from pydantic import BaseModel, EmailStr

from app.schemas.comment import Comment
from app.schemas.post import Post


class UserBase(BaseModel):
    username: str
    email: EmailStr
    auto_reply: bool
    reply_delay: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    auto_reply: bool
    reply_delay: int
    posts: List[Post] = []
    comments: List[Comment] = []

    class Config:
        orm_mode = True
