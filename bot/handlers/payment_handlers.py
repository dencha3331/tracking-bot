import datetime
from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram_dialog import ShowMode, StartMode

from bot_logger import logger
from configs import settings
from db import crud
from db.models import Transaction
from states import MainStateGroup

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from aiogram_dialog import DialogManager
    from aiogram.types import Message, PreCheckoutQuery
    from aiogram.fsm.storage.redis import RedisStorage
    from redis import Redis

    from db.models import User

payments_router: Router = Router()


@payments_router.pre_checkout_query(lambda query: True)
async def checkout(
    pre_checkout_query: "PreCheckoutQuery", db_session: "AsyncSession"
) -> None:
    """Проверка есть ли такая транзакция в бд"""
    transaction: Transaction = await crud.get_current_transaction(
        user_tg_id=pre_checkout_query.from_user.id,
        invoice_payload=pre_checkout_query.invoice_payload,
        db_session=db_session,
    )
    if transaction:
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(
            ok=False,
            error_message="Ошибка при платеже",
        )


@payments_router.message(F.content_type.in_(["successful_payment"]))
async def got_payment(message: "Message", dialog_manager: "DialogManager") -> None:
    """Подтвержденная оплата(сообщение об успешной оплате от телеграмм)"""

    transaction: "Transaction" = await save_payment(message, dialog_manager)

    await unban_user(message=message)

    await delete_invoice_message(dialog_manager, message)

    invite_link = await get_invite_link(message=message, expire_days=transaction.days)

    await dialog_manager.start(
        state=MainStateGroup.main_dialog,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={
            "is_success_payment_message": True,
            "invite_link": invite_link,
        },
    )
    await reset_ending_subscribe_messages_count(
        dialog_manager=dialog_manager,
        telegram_userid=message.from_user.id,
    )


async def unban_user(message: "Message") -> None:
    try:
        await message.bot.unban_chat_member(
            chat_id=settings.telegram.chanel_id, user_id=message.from_user.id
        )
    except TelegramBadRequest as e:
        logger.error(e)
    except Exception as e:
        logger.exception(e)


async def delete_invoice_message(
    dialog_manager: "DialogManager", message: "Message"
) -> None:
    invoice_message_id: int = dialog_manager.dialog_data.get("invoice_message_id")
    if invoice_message_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id, message_id=invoice_message_id
            )
        except TelegramBadRequest:
            pass


async def save_payment(
    message: "Message", dialog_manager: "DialogManager"
) -> "Transaction":
    db_user: "User" = dialog_manager.middleware_data.get("db_user")
    db_session: "AsyncSession" = dialog_manager.middleware_data.get("db_session")

    transaction: "Transaction" = await crud.get_current_transaction(
        user_tg_id=message.from_user.id,
        invoice_payload=message.successful_payment.invoice_payload,
        db_session=db_session,
    )
    transaction.success = True
    if not db_user.start_subscribe or db_user.end_subscribe < datetime.datetime.now():
        db_user.start_subscribe = datetime.datetime.now()
    if not db_user.end_subscribe:
        db_user.end_subscribe = datetime.datetime.now() + datetime.timedelta(
            days=transaction.days
        )
    elif db_user.end_subscribe < datetime.datetime.now():
        db_user.end_subscribe = datetime.datetime.now() + datetime.timedelta(
            days=transaction.days
        )
    elif db_user.end_subscribe > datetime.datetime.now():
        db_user.end_subscribe += datetime.timedelta(days=transaction.days)
    db_user.is_chanel_user = True
    await crud.add_object_to_db_session(
        transaction,
        db_user,
        db_session=db_session,
    )
    return transaction


async def reset_ending_subscribe_messages_count(
    dialog_manager: "DialogManager", telegram_userid: int
) -> None:
    redis_storage: "RedisStorage" = dialog_manager.middleware_data.get("fsm_storage")
    redis: "Redis" = redis_storage.redis
    await redis.set(
        name=f"{telegram_userid}_ending_subscribe_messages_count",
        value=0,
    )


async def get_invite_link(message, expire_days) -> str:
    invite_link = await message.bot.create_chat_invite_link(
        settings.telegram.chanel_id,
        member_limit=1,
        expire_date=datetime.timedelta(days=expire_days),
    )
    return invite_link.invite_link
