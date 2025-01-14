from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import StartMode
from aiogram_dialog.api.exceptions import NoContextError

if TYPE_CHECKING:
    from aiogram.types import Message
    from aiogram.fsm.context import FSMContext
    from aiogram_dialog import DialogManager

    from db.models import User

from states import (
    MainStateGroup,
)
from utils.messages_utils import delete_previous_message, delete_send_inform_message

command_router = Router(name="Command router")


@command_router.message(Command("start"))
async def start(
    message: "Message",
    dialog_manager: "DialogManager",
    state: "FSMContext",
    db_user: "User",
) -> None:

    redis_storage: "RedisStorage" = dialog_manager.middleware_data.get("fsm_storage")

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
    await delete_previous_message(dialog_manager=dialog_manager)
