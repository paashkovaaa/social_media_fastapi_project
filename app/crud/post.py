from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.post import DBPost
from app.schemas.post import PostCreate

from app.utils.moderation import moderate_text


def create_post(db: Session, post: PostCreate, user_id: int) -> DBPost:
    moderation_result_content = moderate_text(post.content)
    moderation_result_title = moderate_text(post.title)

    is_blocked = (
        not moderation_result_content["is_approved"]
        or not moderation_result_title["is_approved"]
    )

    db_post = DBPost(**post.dict(), owner_id=user_id, is_blocked=is_blocked)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    if is_blocked:
        raise HTTPException(
            status_code=400,
            detail="Post contains inappropriate content and is blocked.",
        )
    return db_post


def get_post(db: Session, post_id: int) -> DBPost:
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post and db_post.is_blocked:
        raise HTTPException(status_code=403, detail="This post has been blocked.")
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 10) -> list[DBPost]:
    return (
        db.query(DBPost)
        .filter(DBPost.is_blocked == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_posts_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
) -> list[DBPost]:
    return (
        db.query(DBPost)
        .filter(DBPost.owner_id == user_id, DBPost.is_blocked == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_post(db: Session, post_id: int, post_update: PostCreate) -> DBPost:
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post:
        moderation_result_content = moderate_text(db_post.content)
        moderation_result_title = moderate_text(db_post.title)

        is_blocked = (
            not moderation_result_content["is_approved"]
            or not moderation_result_title["is_approved"]
        )

        db_post.title = post_update.title or db_post.title
        db_post.content = post_update.content or db_post.content
        db.commit()
        db.refresh(db_post)
        if is_blocked:
            raise HTTPException(
                status_code=400,
                detail="Post contains inappropriate content and is blocked.",
            )
    return db_post


def delete_post(db: Session, post_id: int) -> None:
    db.query(DBPost).filter(DBPost.id == post_id).delete()
    db.commit()
