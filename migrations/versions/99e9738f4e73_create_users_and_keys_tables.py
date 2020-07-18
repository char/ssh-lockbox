"""Create users and keys tables

Revision ID: 99e9738f4e73
Revises: 
Create Date: 2020-07-18 01:45:36.201155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "99e9738f4e73"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "keys",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("key_algorithm", sa.String(), nullable=False),
        sa.Column("key_contents", sa.String(), nullable=False),
        sa.Column("key_comment", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("keys")
    op.drop_table("users")
