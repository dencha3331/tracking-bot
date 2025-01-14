from typing import TYPE_CHECKING
import asyncio
import gc

from pyrogram.errors import FloodWait

from bot_logger import get_logger
from src.subscribe_control.by_chat_users import check_users
from src.subscribe_control.by_db_users import check_subscribe

if TYPE_CHECKING:
    from aiogram import Bot
    from redis.asyncio import Redis


logger = get_logger()


async def check_subscribe_by_chat_users():
    while True:
        try:
            await check_users()
        except FloodWait as e:
            logger.error(e)
            await asyncio.sleep(e.value)
        except Exception as e:
            logger.exception(e)
        gc.collect()


async def check_subscribe_by_db_users(bot: "Bot", redis: "Redis"):
    while True:
        await asyncio.sleep(5)
        try:
            await check_subscribe(bot=bot, redis=redis)
        except Exception as e:
            logger.exception(e)
        gc.collect()
