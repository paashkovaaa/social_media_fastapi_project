from alembic import op
import sqlalchemy as sa


revision = "5538d7c7eea8"
down_revision = "cdde90b31cdd"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "comments_new",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("is_blocked", sa.Boolean(), nullable=True),
        sa.Column("parent_comment_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["parent_comment_id"], ["comments.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute(
        "INSERT INTO comments_new (id, content, post_id, owner_id, created_at, is_blocked, parent_comment_id) SELECT id, content, post_id, owner_id, created_at, is_blocked, parent_comment_id FROM comments"
    )

    op.drop_table("comments")

    op.rename_table("comments_new", "comments")


def downgrade():

    pass
