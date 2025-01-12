"""add days column to transactions table

Revision ID: d241ae705261
Revises: c99696865949
Create Date: 2025-01-13 00:27:14.360764

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d241ae705261"
down_revision: Union[str, None] = "c99696865949"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("transactions", sa.Column("days", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("transactions", "days")
