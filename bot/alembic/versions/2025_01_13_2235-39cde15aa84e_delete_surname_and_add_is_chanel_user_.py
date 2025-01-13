"""delete surname and add is_chanel_user columns in users table

Revision ID: 39cde15aa84e
Revises: d241ae705261
Create Date: 2025-01-13 22:35:54.530981

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "39cde15aa84e"
down_revision: Union[str, None] = "d241ae705261"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_chanel_user", sa.Boolean(), nullable=True))
    op.drop_column("users", "surname")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("surname", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("users", "is_chanel_user")
