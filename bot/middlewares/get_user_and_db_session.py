from typing import (
    Callable,
    Dict,
    Any,
    Awaitable,
    TYPE_CHECKING,
)

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import (
    TelegramObject,
    CallbackQuery,
    Message,
)

from db import db_helper, crud

if TYPE_CHECKING:
    from db.models import User
    from sqlalchemy.ext.asyncio import AsyncSession
    from aiogram.types import User as TGUser


class GetUserAndDBSessionMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if (
            isinstance(event, CallbackQuery)
            and event.message.chat.type != ChatType.PRIVATE
        ):
            return
        if isinstance(event, Message) and event.chat.type != ChatType.PRIVATE:
            return
        db_session: "AsyncSession" = await db_helper.session_getter()
        tg_user: "TGUser" = data["event_from_user"]
        db_user: "User | None" = await crud.get_user(
            telegram_userid=tg_user.id,
            db_session=db_session,
        )
        if not db_user:
            db_user = await crud.create_new_user(
                telegram_user=tg_user,
                db_session=db_session,
            )
        data["db_user"] = db_user
        data["db_session"] = db_session

        result = await handler(event, data)

        await db_helper.dispose()

        return result
