import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import DBUser
from app.schemas.user import UserCreate
from app.auth.auth import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_user(db):
    user_in = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="password",
        auto_reply=False,
        reply_delay=0,
    )
    hashed_password = get_password_hash(user_in.password)
    user = DBUser(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        auto_reply=user_in.auto_reply,
        reply_delay=user_in.reply_delay,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
