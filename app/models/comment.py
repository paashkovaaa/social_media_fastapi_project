from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class DBComment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_blocked = Column(Boolean, default=False)
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    post = relationship("DBPost", back_populates="comments")
    owner = relationship("DBUser", back_populates="comments")
    parent_comment = relationship(
        "DBComment", remote_side=[id], back_populates="replies"
    )
    replies = relationship("DBComment", back_populates="parent_comment")
