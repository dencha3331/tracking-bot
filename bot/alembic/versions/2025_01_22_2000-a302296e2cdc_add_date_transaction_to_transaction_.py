"""add date_transaction to transaction table

Revision ID: a302296e2cdc
Revises: 39cde15aa84e
Create Date: 2025-01-22 20:00:42.294954

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a302296e2cdc"
down_revision: Union[str, None] = "39cde15aa84e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "transactions",
        sa.Column("date_transaction", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("transactions", "date_transaction")
