import datetime
import hashlib
import time
from typing import TYPE_CHECKING, Union
from aiogram.types import LabeledPrice
from aiogram_dialog import (
    ShowMode,
)

from db import crud
from states import PaymentStateGroup
from configs import settings
from db.models import Transaction

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
        Message,
    )

    from db.models import User


async def click_subscribe(
    callback: "CallbackQuery",
    button: "Button",
    dialog_manager: Union["SubManager", "DialogManager"],
) -> None:

    db_user: "User" = dialog_manager.middleware_data.get("db_user")
    db_session: "AsyncSession" = dialog_manager.middleware_data.get("db_session")

    if button.widget_id == "go_to_1_month_subscribe":
        amount = 99000
        label = "990 руб на 1 мес"
        days = 30
    elif button.widget_id == "go_to_3_month_subscribe":
        amount = 249000
        label = "2490 руб на 3 мес"
        days = 90
    # elif button.widget_id == "go_to_6_month_subscribe":
    else:
        amount = 499000
        label = "4990 руб на 6 мес"
        days = 180

    str_hash: str = (
        f"{callback.message.from_user.id}{callback.message.message_id}{time.time()}"
    )
    hash_object = hashlib.md5(str_hash.encode())
    hex_dig: str = hash_object.hexdigest()
    payload: str = hex_dig

    transaction = Transaction(
        sum=amount, payload=payload, days=days, user_telegramid=db_user.user_telegramid
    )
    invoice_message: "Message" = await send_invoice(
        message=callback.message,
        amount=amount,
        label=label,
        payload=payload,
    )
    await crud.add_object_to_db_session(transaction, db_session=db_session)
    dialog_manager.dialog_data["invoice_message_id"] = invoice_message.message_id
    await dialog_manager.switch_to(
        PaymentStateGroup.paying, show_mode=ShowMode.DELETE_AND_SEND
    )


async def send_invoice(
    message: "Message", amount: int, label: str, payload: str
) -> "Message":
    bot = message.bot
    prices = [LabeledPrice(label=label, amount=amount)]

    return await bot.send_invoice(
        chat_id=message.chat.id,
        title=label,
        description="Описание счета",
        payload=payload,
        provider_token=settings.telegram.payment_token,
        # is_flexible=False,
        currency="rub",
        prices=prices,
        # start_parameter="test-payment",
    )


async def cancel_button(
    callback: "CallbackQuery",
    button: "Button",
    dialog_manager: Union["SubManager", "DialogManager"],
) -> None:

    db_user: "User" = dialog_manager.middleware_data.get("db_user")
    db_session: "AsyncSession" = dialog_manager.middleware_data.get("db_session")
    await crud.clear_not_pay_user_transactions(
        user_tg_id=db_user.user_telegramid, db_session=db_session
    )
    try:
        await callback.bot.delete_message(
            callback.message.chat.id,
            dialog_manager.dialog_data["invoice_message_id"],
        )
    except Exception as e:
        print(e)
