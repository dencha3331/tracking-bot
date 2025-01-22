from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram_dialog import StartMode
from aiogram_dialog.api.exceptions import NoContextError

from db import crud

if TYPE_CHECKING:
    from aiogram.types import Message
    from aiogram.fsm.context import FSMContext
    from aiogram_dialog import DialogManager

    from db.models import User

from states import (
    MainStateGroup,
)
from utils.messages_utils import delete_previous_message

command_router = Router(name="Command router")


@command_router.message(Command("start"))
async def start(
    message: "Message",
    dialog_manager: "DialogManager",
    state: "FSMContext",
    db_user: "User",
) -> None:

    await clear_chat(message=message, dialog_manager=dialog_manager)
    await state.clear()

    await dialog_manager.start(
        state=MainStateGroup.main_dialog,
        mode=StartMode.RESET_STACK,
    )


async def clear_chat(message: "Message", dialog_manager: "DialogManager"):
    await message.delete()
    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=dialog_manager.dialog_data["previous_message_id"],
        )
    except (TelegramBadRequest, NoContextError, KeyError):
        pass
    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=dialog_manager.dialog_data["message_id"],
        )
    except (TelegramBadRequest, NoContextError, KeyError):
        pass
    try:
        await crud.clear_not_pay_user_transactions(user_tg_id=message.from_user.id)
        if dialog_manager.dialog_data["invoice_message_id"]:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=dialog_manager.dialog_data["invoice_message_id"],
            )
    except (TelegramBadRequest, NoContextError, KeyError):
        pass
    await delete_previous_message(dialog_manager=dialog_manager)
