import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.start_keyboard import menu
from loader import dp, db, bot
video_id="BAACAgIAAxkBAAMIZLQRJUMUfaBg495TkXA-sXg0Ne0AAm8uAAKriKFJ8bKNRBtW57AvBA"
photo_id ="AgACAgIAAxkBAAMGZLQQ7a_4ZnMiTr0IivEQKK4Cn9YAAmLJMRuriKFJZ1KOPEuwo5gBAAMCAAN5AAMvBA"
jshshr_id="AgACAgIAAxkBAAMKZLQRXJWpmD__HyB8VsLE593dEDwAAmXJMRuriKFJDEWzEw8w3bUBAAMCAAN5AAMvBA"
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            state="menu::::"
        )
    except asyncpg.exceptions.UniqueViolationError:
        await db.update_user_state(message.from_user.id,"menu::::")
        user = await db.select_user(telegram_id=message.from_user.id)

    await message.answer_video(video_id,caption=f"<a href=\"https://t.me/renuadmisson/15\">✅Universitet haqida</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/8\">✅Taʼlim yoʻnalishlari</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/57\">✅Kantrakt miqdori</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/18\">✅Imtiyzolar</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/16\">✅Nega ayan biz</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/28\">✅Qabul 2023</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/23\">✅Univertetga qanday boriladi ?</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/26\">✅Kantakt maʼlumotlar</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/25\">✅Lakatsiya</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/27\">✅Hujjat topshirish</a>\n"\
                                 f"<a href=\"https://t.me/renuadmisson/10?single\">✅Litsenziya</a>\n"\
                "1 mlrdlik grant",reply_markup=menu)
    await message.answer_photo(photo=photo_id)
    await message.answer_location(longitude=69.210325, latitude=41.19043)
    # await message.answer(text=f"<a href=\"https://t.me/renuadmisson/15\">✅Universitet haqida</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/8\">✅Taʼlim yoʻnalishlari</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/57\">✅Kantrakt miqdori</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/18\">✅Imtiyzolar</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/16\">✅Nega ayan biz</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/28\">✅Qabul 2023</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/23\">✅Univertetga qanday boriladi ?</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/26\">✅Kantakt maʼlumotlar</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/25\">✅Lakatsiya</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/27\">✅Hujjat topshirish</a>\n"\
    #                              f"<a href=\"https://t.me/renuadmisson/10?single\">✅Litsenziya</a>\n"\
    #             "1 mlrdlik grant",reply_markup=menu, disable_web_page_preview=True)
    # await message.answer(
    #     "Xush kelibsiz!",
    #     reply_markup=menu,
    # )

    # ADMINGA xabar beramiz
    # count = await db.count_users()
    # msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    # await bot.send_message(chat_id=ADMINS[0], text=msg)
