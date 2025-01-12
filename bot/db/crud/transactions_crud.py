from typing import TYPE_CHECKING

from sqlalchemy import select, delete, and_

from db.models import Transaction

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_transaction(
    user_tg_id,
    invoice_payload,
    db_session: "AsyncSession",
):
    stmt = (
        select(Transaction)
        .where(Transaction.user_telegramid == int(user_tg_id))
        .where(Transaction.payload == invoice_payload)
    )
    async with db_session as session:
        result = await session.scalars(stmt)
        transaction = result.one_or_none()

        return transaction


async def clear_not_pay_user_transactions(
    user_tg_id,
    db_session: "AsyncSession",
):
    stmt = delete(Transaction).where(
        and_(
            Transaction.user_telegramid == user_tg_id,
            Transaction.success.is_(False),
        )
    )
    async with db_session as session:
        await session.execute(stmt)
        await session.commit()
