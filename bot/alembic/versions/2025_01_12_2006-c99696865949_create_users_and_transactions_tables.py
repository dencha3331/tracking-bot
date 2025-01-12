"""create users and transactions tables

Revision ID: c99696865949
Revises: 
Create Date: 2025-01-12 20:06:59.464285

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c99696865949"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_telegramid", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("firstname", sa.String(), nullable=True),
        sa.Column("lastname", sa.String(), nullable=True),
        sa.Column("surname", sa.String(), nullable=True),
        sa.Column(
            "first_contact_date",
            sa.Date(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("start_subscribe", sa.DateTime(), nullable=True),
        sa.Column("end_subscribe", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_telegramid"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sum", sa.Integer(), nullable=False),
        sa.Column("payload", sa.String(), nullable=False),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("user_telegramid", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_telegramid"],
            ["users.user_telegramid"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("payload"),
    )


def downgrade() -> None:
    op.drop_table("transactions")
    op.drop_table("users")
