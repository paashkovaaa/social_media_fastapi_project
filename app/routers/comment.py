from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.models.user import DBUser
from app.schemas.comment import CommentCreate, Comment
from app.crud.comment import (
    create_comment,
    get_comment,
    get_comments_by_user,
    get_comments_by_post,
    delete_comment,
    get_comment_analytics,
    get_replies_by_comment,
)
from app.database import get_db
from app.auth.auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=Comment)
def create_comment_endpoint(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    return create_comment(db, comment, current_user.id)


@router.get("/{comment_id}", response_model=Comment)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = get_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.get("/user/{user_id}", response_model=List[Comment])
def read_comments_by_user(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return get_comments_by_user(db, user_id, skip=skip, limit=limit)


@router.get("/post/{post_id}", response_model=List[Comment])
def read_comments_by_post(
    post_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return get_comments_by_post(db, post_id, skip=skip, limit=limit)


@router.get("/replies/{comment_id}", response_model=List[Comment])
def read_replies_by_comment(comment_id: int, db: Session = Depends(get_db)):
    replies = get_replies_by_comment(db, comment_id)
    return replies


@router.delete("/{comment_id}")
def delete_comment_endpoint(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    db_comment = get_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this comment"
        )
    delete_comment(db, comment_id)
    return {"detail": "Comment deleted"}


@router.get("/analytics/comments-daily-breakdown")
async def get_comments_daily_breakdown(
    date_from: datetime = Query(
        ..., description="Start date for the period (YYYY-MM-DD)"
    ),
    date_to: datetime = Query(..., description="End date for the period (YYYY-MM-DD)"),
    db_session: Session = Depends(get_db),
):
    analytics = get_comment_analytics(db_session, date_from, date_to)
    return analytics
