"""Create integrations table

Revision ID: 4997a5924512
Revises: 836f80f48e09
Create Date: 2020-07-27 03:55:32.781227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4997a5924512"
down_revision = "836f80f48e09"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_integrations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("integration_type", sa.String(), nullable=False),
        sa.Column("integration_domain", sa.String(), nullable=False),
        sa.Column("integration_data", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("user_integrations")
