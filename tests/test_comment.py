import pytest

from app.crud.post import create_post
from app.models.post import DBPost
from app.models.comment import DBComment
from app.schemas.comment import CommentCreate
from app.crud.comment import (
    create_comment,
    get_comment,
    get_comments_by_post,
    get_replies_by_comment,
    get_comment_analytics,
)
from datetime import datetime

from app.schemas.post import PostCreate


def test_create_comment(db, test_user):
    post = DBPost(
        title="Test Post", content="This is a test post", owner_id=test_user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    comment_in = CommentCreate(content="This is a test comment", post_id=post.id)
    comment = create_comment(db, comment_in, test_user.id)
    assert comment.content == "This is a test comment"
    assert comment.post_id == post.id
    assert comment.owner_id == test_user.id


def test_get_comment(db, test_user):
    post = DBPost(
        title="Test Post", content="This is a test post", owner_id=test_user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    comment = DBComment(
        content="This is a test comment", post_id=post.id, owner_id=test_user.id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    retrieved_comment = get_comment(db, comment.id)
    assert retrieved_comment.id == comment.id
    assert retrieved_comment.content == "This is a test comment"


def test_get_comments_by_post(db, test_user):
    post = DBPost(
        title="Test Post", content="This is a test post", owner_id=test_user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    comment1 = DBComment(
        content="First comment", post_id=post.id, owner_id=test_user.id
    )
    comment2 = DBComment(
        content="Second comment", post_id=post.id, owner_id=test_user.id
    )
    db.add(comment1)
    db.add(comment2)
    db.commit()

    comments = get_comments_by_post(db, post.id)
    assert len(comments) == 2
    assert comments[0].content == "First comment"
    assert comments[1].content == "Second comment"


def test_get_replies_by_comment(db, test_user):
    post_in = PostCreate(title="Test Post", content="This is a test post")
    post = create_post(db, post_in, test_user.id)

    parent_comment_in = CommentCreate(content="Parent comment", post_id=post.id)
    parent_comment = create_comment(db, parent_comment_in, test_user.id)

    reply_in = CommentCreate(
        content="Reply comment", post_id=post.id, parent_comment_id=parent_comment.id
    )
    create_comment(db, reply_in, test_user.id)

    replies = get_replies_by_comment(db, parent_comment.id)

    assert len(replies) == 1
    assert replies[0].content == "Reply comment"
    assert replies[0].parent_comment_id == parent_comment.id


def test_get_comment_analytics(db, test_user):
    post = DBPost(
        title="Test Post", content="This is a test post", owner_id=test_user.id
    )
    db.add(post)
    db.commit()

    today = datetime.utcnow()
    comment1 = DBComment(content="Comment 1", post_id=post.id, created_at=today)
    comment2 = DBComment(
        content="Comment 2", post_id=post.id, created_at=today, is_blocked=True
    )
    db.add(comment1)
    db.add(comment2)
    db.commit()

    date_from = today
    date_to = today

    analytics = get_comment_analytics(db, date_from, date_to)
    assert len(analytics) == 1
    assert analytics[0].created_comments == 2
    assert analytics[0].blocked_comments == 1
