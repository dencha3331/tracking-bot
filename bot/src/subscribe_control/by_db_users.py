import datetime

from aiogram import Bot
from aiogram.types import User as TGUser, Chat
from aiogram_dialog import StartMode, ShowMode
from aiogram_dialog.manager.bg_manager import BgManager

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from bot_logger import get_logger
from configs import settings
from db import db_helper, crud
from db.models import User
from dialogs import main_dialog
from states import MainStateGroup
from utils.kick_user_from_chat import kick_user

logger = get_logger()


async def check_subscribe(bot: "Bot", redis: "Redis"):

    db_session: "AsyncSession" = await db_helper.session_getter()
    chanel_users: list["User"] = await crud.get_chanel_users(db_session=db_session)
    for db_user in chanel_users:
        logger.info(f"{db_user.firstname}")
        if db_user.end_subscribe and db_user.end_subscribe < datetime.datetime.now():
            try:
                await kick_user(
                    tg_userid=db_user.user_telegramid,
                    chat_id=settings.telegram.chanel_id,
                    app=bot,
                )
            except Exception as e:
                logger.exception(e)
        information_message = await _get_inform_message(user=db_user, redis=redis)
        if not information_message:
            continue
        await _send_subscribe_info_message(
            bot=bot,
            db_user=db_user,
            information_message=information_message,
        )


async def _get_inform_message(user: "User", redis: "Redis") -> str:
    ending_subscribe_messages_count = await redis.get(
        f"{user.user_telegramid}_ending_subscribe_messages_count"
    )
    ending_subscribe_messages_count = (
        int(ending_subscribe_messages_count)
        if ending_subscribe_messages_count
        else ending_subscribe_messages_count
    )
    if user.end_subscribe and user.end_subscribe < datetime.datetime.now():
        if (
            ending_subscribe_messages_count is not None
            and ending_subscribe_messages_count <= 3
        ):
            await _set_messages_count_value(redis, user, 4)
            return "К сожалению Ваша подписка закончилась. Надеемся Вы к нам вернетесь."
    elif (
        user.end_subscribe
        and user.end_subscribe < datetime.datetime.now() + datetime.timedelta(hours=3)
    ):
        if (
            ending_subscribe_messages_count is not None
            and ending_subscribe_messages_count <= 2
        ):
            await _set_messages_count_value(redis, user, 3)
            return (
                "Ваша подписка закончится через 3 часа. "
                "Вы всегда можете ее продлить по кнопке ниже."
            )
    elif (
        user.end_subscribe
        and user.end_subscribe < datetime.datetime.now() + datetime.timedelta(days=1)
    ):
        if (
            ending_subscribe_messages_count is not None
            and ending_subscribe_messages_count <= 1
        ):
            await _set_messages_count_value(redis, user, 2)
            return (
                "Ваша подписка завтра заканчивается. "
                "Вы всегда можете ее продлить по кнопке ниже."
            )
    elif (
        user.end_subscribe
        and user.end_subscribe < datetime.datetime.now() + datetime.timedelta(days=3)
    ):
        if not ending_subscribe_messages_count:
            await _set_messages_count_value(redis, user, 1)
            return (
                "Ваша подписка заканчивается через 3 дня. "
                "Вы всегда можете ее продлить по кнопке ниже."
            )


async def _set_messages_count_value(redis: "Redis", user: "User", value: int):
    await redis.set(
        name=f"{user.user_telegramid}_ending_subscribe_messages_count",
        value=value,
    )


async def _send_subscribe_info_message(
    bot: "Bot", db_user: "User", information_message: str
) -> None:
    tg_user = TGUser(
        id=db_user.user_telegramid,
        is_bot=False,
        first_name=db_user.firstname,
    )
    chat = Chat(id=db_user.user_telegramid, type="private")
    manager = BgManager(
        user=tg_user,
        chat=chat,
        bot=bot,
        router=main_dialog,
        intent_id=None,
        stack_id="",
        load=True,
    )
    await manager.start(
        state=MainStateGroup.main_dialog,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={
            "information_message": information_message,
        },
    )
