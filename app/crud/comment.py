from datetime import datetime
from typing import List

from sqlalchemy import func, case
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.comment import DBComment
from app.models.post import DBPost
from app.models.user import DBUser
from app.schemas.comment import CommentCreate, CommentAnalytics
from app.utils.auto_reply import generate_ai_reply
from app.utils.moderation import moderate_text


def create_comment(db: Session, comment: CommentCreate, user_id: int) -> DBComment:
    moderation_result = moderate_text(comment.content)
    is_blocked = not moderation_result["is_approved"]

    db_comment = DBComment(
        content=comment.content,
        post_id=comment.post_id,
        owner_id=user_id,
        is_blocked=is_blocked,
        parent_comment_id=comment.parent_comment_id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    if is_blocked:
        raise HTTPException(
            status_code=400,
            detail="Comment contains inappropriate content and is blocked.",
        )

    post = db.query(DBPost).filter(DBPost.id == comment.post_id).first()
    post_content = post.content if post else ""

    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user and user.auto_reply:
        ai_reply = generate_ai_reply(post_content, comment.content, user_id, db)

        db_reply = DBComment(
            content=ai_reply,
            post_id=comment.post_id,
            owner_id=user_id,
            is_blocked=False,
            parent_comment_id=db_comment.id,
        )
        db.add(db_reply)
        db.commit()
        db.refresh(db_reply)

    return db_comment


def get_comment(db: Session, comment_id: int) -> DBComment:
    db_comment = db.query(DBComment).filter(DBComment.id == comment_id).first()
    if db_comment and db_comment.is_blocked:
        raise HTTPException(status_code=403, detail="This comment has been blocked.")
    return db_comment


def get_comments_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
) -> list[DBComment]:
    return (
        db.query(DBComment)
        .filter(DBComment.owner_id == user_id, DBComment.is_blocked == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_comments_by_post(
    db: Session, post_id: int, skip: int = 0, limit: int = 10
) -> list[DBComment]:
    return (
        db.query(DBComment)
        .filter(DBComment.post_id == post_id, DBComment.is_blocked == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_replies_by_comment(db: Session, comment_id: int) -> list[DBComment]:
    return (
        db.query(DBComment)
        .filter(
            DBComment.parent_comment_id == comment_id, DBComment.is_blocked == False
        )
        .all()
    )


def delete_comment(db: Session, comment_id: int) -> None:
    db.query(DBComment).filter(DBComment.id == comment_id).delete()
    db.commit()


def get_comment_analytics(
    db_session: Session, date_from: datetime, date_to: datetime
) -> List[CommentAnalytics]:
    """
    This function retrieves comment analytics for a specific period.

    Args:
        db_session: SQLAlchemy session object.
        date_from: Start date for the analysis period (inclusive).
        date_to: End date for the analysis period (inclusive).

    Returns:
        A list of CommentAnalytics objects, one for each day in the period.
    """
    query = (
        db_session.query(
            func.date(DBComment.created_at).label("date"),
            func.count(DBComment.id).label("created_comments"),
            func.sum(case((DBComment.is_blocked == True, 1), else_=0)).label(
                "blocked_comments"
            ),
        )
        .filter(DBComment.created_at >= date_from, DBComment.created_at <= date_to)
        .group_by(func.date(DBComment.created_at))
        .order_by(func.date(DBComment.created_at))
        .all()
    )
    return [
        CommentAnalytics(date=row[0], created_comments=row[1], blocked_comments=row[2])
        for row in query
    ]
