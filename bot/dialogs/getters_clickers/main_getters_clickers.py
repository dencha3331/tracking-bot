import datetime
from typing import TYPE_CHECKING, Union

# from db import crud

if TYPE_CHECKING:
    from aiogram import Bot
    from redis.asyncio.client import Redis
    from aiogram.fsm.storage.redis import RedisStorage
    from aiogram_dialog.widgets.kbd import Button
    from aiogram_dialog.widgets.common import Whenable
    from sqlalchemy.ext.asyncio import AsyncSession
    from aiogram_dialog import (
        DialogManager,
        SubManager,
    )
    from aiogram.types import (
        CallbackQuery,
    )

    from db.models import User


async def main_menu_getter(dialog_manager: "DialogManager", **kwargs) -> dict:
    db_user: "User" = dialog_manager.middleware_data.get("db_user")
    not_subscribe_user = db_user.end_subscribe is None
    information_message = None
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
        information_message = f"Вы успешно оформили подписку ✅"
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
