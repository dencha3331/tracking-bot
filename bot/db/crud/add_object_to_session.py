from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from db.db_helper import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from db.models import Base


async def add_object_to_db_session(
    *objs: "Base",
    db_session: "AsyncSession" = None,
) -> None:
    if not db_session:
        db_session = await db_helper.session_getter()

    async with db_session as session:
        try:
            session.add_all(objs)
            await session.commit()
        except (Exception, IntegrityError) as e:
            print(f"add_object_to_db_session: {e!r}")
