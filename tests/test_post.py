import pytest
from app.models.post import DBPost
from app.schemas.post import PostCreate
from app.crud.post import create_post, get_post, update_post, delete_post


def test_create_post(db, test_user):
    post_in = PostCreate(title="Test Post", content="This is a test post")
    post = create_post(db, post_in, test_user.id)
    assert post.title == "Test Post"
    assert post.content == "This is a test post"
    assert post.owner_id == test_user.id


def test_get_post(db, test_user):
    post = DBPost(
        title="Test Post", content="This is a test post", owner_id=test_user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    retrieved_post = get_post(db, post.id)
    assert retrieved_post.id == post.id
    assert retrieved_post.title == "Test Post"


def test_update_post(db, test_user):
    post_in = PostCreate(title="Original Title", content="Original Content")
    post = create_post(db, post_in, test_user.id)

    post_update = PostCreate(title="Updated Title", content="Updated Content")
    updated_post = update_post(db, post.id, post_update)

    assert updated_post.title == "Updated Title"
    assert updated_post.content == "Updated Content"


def test_delete_post(db, test_user):
    post_in = PostCreate(title="Test Post", content="This is a test post")
    post = create_post(db, post_in, test_user.id)

    delete_post(db, post.id)
    deleted_post = db.query(DBPost).filter(DBPost.id == post.id).first()
    assert deleted_post is None
