import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from redis.asyncio.client import Redis
from aiogram.fsm.storage.redis import RedisStorage

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


async def main():
    redis: Redis = Redis(host=settings.redis.host, port=settings.redis.port, db=5)
    storage: RedisStorage = RedisStorage(
        redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    # await redis.flushall()
    # storage = MemoryStorage()
    bot = Bot(token=settings.telegram.token)
    dp = Dispatcher(storage=storage)

    dp.message.middleware(GetUserAndDBSessionMiddleware())
    dp.callback_query.middleware(GetUserAndDBSessionMiddleware())

    dp.include_routers(
        command_router,
        main_dialog,
        payments_router,
        payment_dialog,
        message_delete_router,
    )

    setup_dialogs(dp)

    print("bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
