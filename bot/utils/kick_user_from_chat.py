import datetime
from typing import TYPE_CHECKING, Union

from bot_logger import logger
from db import crud, db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from aiogram import Bot
    from pyrogram import Client

    from db.models import User


async def kick_user(
    tg_userid: int, chat_id: int, app: Union["Bot", "Client"], ban: bool = True
) -> None:
    until_date = (
        None if ban else datetime.datetime.now() + datetime.timedelta(seconds=40)
    )
    db_session: "AsyncSession" = await db_helper.session_getter()
    user: "User" = await crud.get_user(telegram_userid=tg_userid, db_session=db_session)
    try:
        await app.ban_chat_member(
            chat_id=chat_id,
            user_id=tg_userid,
            until_date=until_date,
        )
        logger.info(f"{tg_userid} BAN")
    except Exception as e:
        logger.exception(e)
    if user:
        user.is_chanel_user = False
        await crud.add_object_to_db_session(user, db_session=db_session)
        logger.info(f"{user.firstname} BAN")
