from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .post import DBPost
from app.database import Base


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    auto_reply = Column(Boolean, default=False)
    reply_delay = Column(Integer, default=60)

    posts = relationship("DBPost", back_populates="owner")
    comments = relationship("DBComment", back_populates="owner")
