from sqlalchemy.orm import Session
from app.models.user import DBUser
from app.schemas.user import UserCreate
from app.auth.auth import verify_password, get_password_hash


def create_user(db: Session, user: UserCreate, hashed_password: str):
    db_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        auto_reply=user.auto_reply,
        reply_delay=user.reply_delay,
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


def update_user(db: Session, user_id: int, user_update: UserCreate):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user:
        if user_update.username:
            db_user.username = user_update.username
        if user_update.email:
            db_user.email = user_update.email
        if user_update.password:
            db_user.hashed_password = get_password_hash(user_update.password)
        if user_update.auto_reply:
            db_user.auto_reply = user_update.auto_reply
        if user_update.reply_delay:
            db_user.reply_delay = user_update.reply_delay
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None
