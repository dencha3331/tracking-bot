from aiogram import Router
from aiogram.types import Message

message_delete_router = Router(name="message delete router")


@message_delete_router.message()
async def delete_not_handle_message(message: Message) -> None:
    if message.chat.type == "private":
        await message.delete()
