from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    post_id: int
    parent_comment_id: int | None = None


class CommentCreate(CommentBase):
    pass


class CommentAnalytics(BaseModel):
    date: datetime
    created_comments: int
    blocked_comments: int


class Comment(CommentBase):
    id: int
    owner_id: int
    is_blocked: bool

    class Config:
        orm_mode = True
