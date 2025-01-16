from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
)


async def set_main_menu(bot: Bot):
    """Set list command menu button"""
    main_menu_commands = [
        BotCommand(command="/start", description="Главное меню 🏡"),
    ]

    await bot.set_my_commands(
        main_menu_commands, scope=BotCommandScopeAllPrivateChats()
    )
