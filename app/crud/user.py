from sqlalchemy.orm import Session
from app.models.user import DBUser
from app.schemas.user import UserCreate
from app.auth.auth import verify_password


def create_user(db: Session, user: UserCreate, hashed_password: str):
    db_user = DBUser(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(DBUser).filter(DBUser.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(DBUser).filter(DBUser.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user
