import datetime
from typing import TYPE_CHECKING, Union

from utils.messages_utils import delete_send_inform_message

if TYPE_CHECKING:
    from aiogram import Bot
    from redis.asyncio.client import Redis
    from aiogram.fsm.storage.redis import RedisStorage
    from aiogram_dialog import DialogManager
    from aiogram.types import CallbackQuery

    from db.models import User


async def main_menu_getter(dialog_manager: "DialogManager", **kwargs) -> dict:
    db_user: "User" = dialog_manager.middleware_data.get("db_user")
    redis_storage: "RedisStorage" = dialog_manager.middleware_data.get("fsm_storage")
    redis: "Redis" = redis_storage.redis
    bot: "Bot" = dialog_manager.middleware_data.get("bot")
    await delete_send_inform_message(
        telegram_userid=db_user.user_telegramid,
        redis=redis,
        bot=bot,
    )
    not_subscribe_user = db_user.end_subscribe is None
    information_message = ""
    is_subscribe_user = (
        db_user.end_subscribe > datetime.datetime.now()
        if db_user.end_subscribe
        else None
    )
    end_subscribe_user = (
        db_user.end_subscribe < datetime.datetime.now()
        if db_user.end_subscribe
        else None
    )
    if dialog_manager.start_data and dialog_manager.start_data.get("invite_link"):
        information_message += f"Вы успешно оформили подписку ✅\n"
    if dialog_manager.start_data and dialog_manager.start_data.get(
        "information_message"
    ):
        information_message += dialog_manager.start_data.get("information_message")

    return {
        "information_message": information_message,
        "is_subscribe_user": is_subscribe_user,
        "end_subscribe_user": end_subscribe_user,
        "not_subscribe_user": not_subscribe_user,
        "invite_link": (
            dialog_manager.start_data.get("invite_link")
            if dialog_manager.start_data
            else None
        ),
        "end_subscribe": (
            db_user.end_subscribe.strftime("%d.%m.%Y %H:%M")
            if db_user.end_subscribe
            else None
        ),
    }


async def cancel_button(
    callback: "CallbackQuery",
    _,
    dialog_manager: "DialogManager",
) -> None:
    if dialog_manager.start_data:
        dialog_manager.start_data["information_message"] = ""
