"""Create access keys table

Revision ID: 836f80f48e09
Revises: 99e9738f4e73
Create Date: 2020-07-20 19:17:52.050671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "836f80f48e09"
down_revision = "99e9738f4e73"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "access_keys",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("access_key_description", sa.String(), nullable=False),
        sa.Column("access_key_token", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("access_keys")
