from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.post import (
    create_post,
    get_post,
    get_posts,
    get_posts_by_user,
    update_post,
    delete_post,
)
from app.schemas.post import PostCreate, Post
from app.auth.auth import get_current_active_user, get_db
from app.models.user import DBUser

router = APIRouter()


@router.post("/", response_model=Post)
def create_post_endpoint(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    return create_post(db, post, current_user.id)


@router.get("/", response_model=list[Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = get_posts(db, skip, limit)
    return posts


@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.get("/user/{user_id}", response_model=list[Post])
def read_posts_by_user(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    posts = get_posts_by_user(db, user_id, skip, limit)
    return posts


@router.put("/{post_id}", response_model=Post)
def update_post_endpoint(
    post_id: int,
    post_update: PostCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    db_post = get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this post"
        )
    return update_post(db, post_id, post_update)


@router.delete("/{post_id}")
def delete_post_endpoint(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    db_post = get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this post"
        )
    delete_post(db, post_id)
    return {"detail": "Post deleted"}
