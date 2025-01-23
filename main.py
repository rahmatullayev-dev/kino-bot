import asyncio
from routers import user, admin
from aiogram import Bot, Dispatcher

import config

dp = Dispatcher()

async def main():
    bot = Bot(token=config.TOKEN)
    dp.include_router(admin.router)
    dp.include_router(user.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Bot ishga tushirildi..")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi..")
        asyncio.sleep(5)