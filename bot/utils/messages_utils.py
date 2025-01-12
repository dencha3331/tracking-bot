from typing import TYPE_CHECKING

from aiogram.exceptions import TelegramBadRequest

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import Chat
    from aiogram_dialog import DialogManager
    from aiogram_dialog.api.entities import Stack
    from redis.asyncio import Redis


async def delete_previous_message(dialog_manager: "DialogManager") -> None:
    if dialog_manager:
        middleware_data: dict = dialog_manager.middleware_data
        if middleware_data:
            stack: Stack = middleware_data.get("aiogd_stack")
            last_message_id = stack.last_message_id
            chat: Chat = middleware_data.get("event_chat")
            bot: Bot = middleware_data.get("bot")
            if bot and last_message_id and chat:
                try:
                    await bot.delete_message(
                        chat_id=chat.id,
                        message_id=last_message_id,
                    )
                except TelegramBadRequest:
                    pass


async def delete_send_inform_message(
    telegram_userid: int, redis: "Redis", bot: "Bot"
) -> None:
    inform_message_id = await redis.get(f"{telegram_userid}_inform_message_id")
    if inform_message_id:
        try:
            await bot.delete_message(
                chat_id=telegram_userid,
                message_id=int(inform_message_id),
            )
        except Exception:
            pass

    inform_message = await bot.send_message(
        chat_id=telegram_userid,
        text="Чтобы разослать сообщение:\n\n"
        "1. Нажать на кнопку - Собрать/обновить чаты.\n"
        "2. Нажать на кнопку - 💬 Все чаты 💬 - выбрать Доверительные (и, если уверены - Сомнительные тоже) и "
        "выбрать пользователей, кому пойдёт рассылка.\n"
        "3. Нажать на кнопку отправить сообщение - ввести сообщение, которое вы хотите разослать.\n"
        "4. Нажать отправить.\n\n"
        "👍 Доверительные - это те, кто вас добавил в адресную книгу, а вы его, "
        "либо кто вам прислал не менее 5 сообщений не более 30 дней назад.\n\n"
        "🤔 Сомнительные - это те собеседники, с кем контакт был более месяца назад и вас "
        "в свою адресную книгу не добавил. Рассылка по Сомнительным может привести к претензиям от "
        "собеседников и временным ограничениям Вашего аккаунта Телеграмом."
        "\n\n ———————————————————\n\n",
    )

    await redis.set(
        name=f"{telegram_userid}_inform_message_id",
        value=inform_message.message_id,
    )


async def delete_inform_message(
    telegram_userid: int, redis: "Redis", bot: "Bot"
) -> None:
    inform_message_id = await redis.get(f"{telegram_userid}_inform_message_id")
    if inform_message_id:
        try:
            await bot.delete_message(
                chat_id=telegram_userid,
                message_id=int(inform_message_id),
            )
            await redis.delete(f"{telegram_userid}_inform_message_id")
        except Exception:
            pass
