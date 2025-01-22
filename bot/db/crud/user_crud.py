from typing import TYPE_CHECKING

from sqlalchemy import select, update

from db import db_helper
from db.models import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from aiogram.types import User as UserTG


async def get_user(
    telegram_userid: int,
    db_session: "AsyncSession" = None,
) -> User | None:
    if not db_session:
        db_session = await db_helper.session_getter()

    stmt = select(User).where(User.user_telegramid == telegram_userid)
    async with db_session as session:
        result = await session.scalars(stmt)
        return result.one_or_none()


async def get_chanel_users(db_session: "AsyncSession" = None) -> list["User"]:
    if not db_session:
        db_session = await db_helper.session_getter()

    stmt = select(User).where(User.is_chanel_user.is_(True))
    async with db_session as session:
        result = await session.scalars(stmt)
        return list(result.all())


async def create_new_user(
    telegram_user: "UserTG",
    db_session: "AsyncSession" = None,
) -> User:
    if not db_session:
        db_session = await db_helper.session_getter()

    user = User(
        user_telegramid=telegram_user.id,
        username=telegram_user.username,
        firstname=telegram_user.first_name,
        lastname=telegram_user.last_name,
    )
    async with db_session as session:
        session.add(user)
        await session.commit()
        return user


async def update_user(
    telegram_userid: int,
    db_session: "AsyncSession" = None,
    **kwargs,
) -> None:
    if not db_session:
        db_session = await db_helper.session_getter()

    stmt = update(User).values(kwargs).where(User.user_telegramid == telegram_userid)
    async with db_session as session:
        try:
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            print(f"{e!r}")
