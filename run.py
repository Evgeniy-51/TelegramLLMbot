import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.menu_kb import set_main_menu


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    await set_main_menu(bot)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("-- Bot stopped --")
