from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from db.models import User

message_delete_router = Router(name="message delete router")


@message_delete_router.message()
async def delete_not_handle_message(message: Message) -> None:
    if message.chat.type == "private":
        await message.delete()
