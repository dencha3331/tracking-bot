from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from db.models import Base


async def add_object_to_db_session(
    *objs: "Base",
    db_session: "AsyncSession",
):
    async with db_session as session:
        try:
            session.add_all(objs)
            await session.commit()
        except (Exception, IntegrityError) as e:
            print(f"add_object_to_db_session: {e!r}")
