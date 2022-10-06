"""Add `levels` table

Revision ID: d29cc0af149e
Revises: b8a31b256f23
Create Date: 2022-10-06 03:18:23.365191
"""

from alembic import op
from sqlalchemy import Column, BigInteger


# revision identifiers, used by Alembic.
revision = "d29cc0af149e"
down_revision = "b8a31b256f23"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "levels",
        Column("id", BigInteger(), primary_key=True),
        Column("experience", BigInteger(), default=0, nullable=False),
    )


def downgrade():
    op.drop_table("levels")
