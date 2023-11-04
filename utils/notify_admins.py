import logging

from aiogram import Dispatcher

from data.config import DEVELOPER


async def on_startup_notify(dp: Dispatcher):
    for admin in DEVELOPER:
        try:

            await dp.bot.send_message(admin, "Bot ishga tushdi")

        except Exception as err:
            logging.exception(err)
