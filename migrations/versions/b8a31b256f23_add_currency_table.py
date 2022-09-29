"""Add currency table

Revision ID: b8a31b256f23
Revises:
Create Date: 2022-09-29 21:59:59.639100
"""

from alembic import op
from sqlalchemy import Column, BigInteger


# revision identifiers, used by Alembic.
revision = "b8a31b256f23"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "currency",
        Column("user_id", BigInteger(), primary_key=True),
        Column("balance", BigInteger(), default=0, nullable=False),
    )


def downgrade():
    op.drop_table("currency")
