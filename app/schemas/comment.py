from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created_at: datetime
    is_blocked: bool
    owner_id: int
    post_id: int

    class Config:
        orm_mode = True
