import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio.client import Redis
from aiogram.fsm.storage.redis import RedisStorage

from bot_logger import get_logger
from configs import settings
from middlewares.get_user_and_db_session import GetUserAndDBSessionMiddleware
from handlers import (
    command_router,
    message_delete_router,
    payments_router,
)
from dialogs import (
    main_dialog,
    payment_dialog,
)
from src.scheduler.parallel_tasks import (
    check_subscribe_by_chat_users,
    check_subscribe_by_db_users,
)


logger = get_logger()


@logger.catch(level="INFO")
async def main():
    redis: Redis = Redis(host=settings.redis.host, port=settings.redis.port, db=5)
    storage: RedisStorage = RedisStorage(
        redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    bot = Bot(token=settings.telegram.token)
    dp = Dispatcher(storage=storage)

    dp.update.middleware(GetUserAndDBSessionMiddleware())

    dp.include_routers(
        command_router,
        payments_router,
        message_delete_router,
        main_dialog,
        payment_dialog,
    )

    setup_dialogs(dp)

    logger.info("bot started")
    d = asyncio.create_task(check_subscribe_by_chat_users())
    a = asyncio.create_task(check_subscribe_by_db_users(bot=bot, redis=redis))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
