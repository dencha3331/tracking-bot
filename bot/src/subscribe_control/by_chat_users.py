from typing import TYPE_CHECKING
import asyncio
import datetime

from pyrogram import Client, enums

from bot_logger import get_logger
from configs import settings
from db import db_helper, crud
from utils.kick_user_from_chat import kick_user

if TYPE_CHECKING:
    from db.models import User
    from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger()


async def check_users():
    async with Client(
        f"{settings.pyrofork.sessions_workdir}tracking_bot",
        api_id=settings.pyrofork.app_id,
        api_hash=settings.pyrofork.app_hash,
        bot_token=settings.telegram.token,
    ) as app:
        async for member in app.get_chat_members(
            settings.telegram.chanel_id
        ):  # type: "ChatMember"
            db_session: "AsyncSession" = await db_helper.session_getter()
            await asyncio.sleep(1)
            if member.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                continue

            user: "User" = await crud.get_user(
                telegram_userid=member.user.id, db_session=db_session
            )
            if (
                not user
                or not user.end_subscribe
                or user.end_subscribe < datetime.datetime.now()
            ):
                try:
                    await kick_user(
                        tg_userid=member.user.id,
                        chat_id=settings.telegram.chanel_id,
                        app=app,
                    )
                    logger.info(f"BAN {member.user.id}, {member.user.first_name}")
                except Exception as e:
                    logger.exception(e)
