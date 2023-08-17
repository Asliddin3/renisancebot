import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.start_keyboard import menu
from loader import dp, db, bot
video_id="BAACAgIAAxkBAAEBEktkzR61Jl98Fv4Oa7JZ-rA58JIvDAACXS8AAggwSUprpgdrbeO8rC8E"
photo_id ="AgACAgIAAxkBAAMRZLdz6r4QA00ijBspTR4iOf8FDOgAAhTGMRtbG8FJRZd5gY8LhMABAAMCAAN5AAMvBA"
jshshr_id="AgACAgIAAxkBAAMVZLd0XImfh0Agvl_Y0WLzt1h1ovwAAhXGMRtbG8FJN2xN2--cwsgBAAMCAAN5AAMvBA"
contract_id="AgACAgIAAxkBAAEBEk9kzR7ahOdESywpuAABF1dYlBxyjRQAAq7MMRsPvGhK-ThtN-GNv8kBAAMCAAN4AAMvBA"
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

    await message.answer_video(video_id,
                               caption="<a href='https://t.me/renuadmission/19'>Universitet haqida batafsil</a>\n\n" \
                                       "<a href='https://t.me/renuadmission/85'>Xususiy oliygohlar diplimi haqida batafsil</a>\n\n" \
                                       "<a href='https://t.me/renuadmission/86'>Baklavr va Magistratura yoʻnlishlari haqida batafsil (har bir yoʻnalishda nimalar oʻrgatiladi ? Asosiy fanlar qaysilar ?)</a>\n\n" \
                                       "Telefonlar:\n" \
                                       "+998947405220  Komila\n" \
                                       "+998947406220  Sarvinoz\n" \
                                       "+998947407220  Diyora\n" \
                                       "+998911357797  Sarvinoz\n" \
                                       "@renuqabul2023\n" \
                                       "@Renuadmin2\n" \
                                       "@Renaissance7220\n" \
                                       "@Renuadmin3\n" \
                                       "Xujjat topshirish uchun @renutestbot", reply_markup=menu)
    await message.answer_photo(photo=photo_id)
    await message.answer_location(longitude=69.210325, latitude=41.19043,)
    await message.answer_photo(photo=contract_id)
    await message.answer(text="Universtetimizga quyidagi lakatsiya orqali yoki 131/58/47/62 yoʻnalishli avtobuslarning oxirgi bekatiga tushib kelishingiz mumkin")
    # await message.answer(text="RENAISSANCE UNIVERSITYda 500 ta grant oʻrinlari mavjud boʻlib 1 semestrni aʼlo bahoga tamomlagan talabalar oʻrtasida qoʻshimcha saralash yoʻli bilan eng yuqori bal olganlarga 2 semestrdan taqdim etiladi")
    # await message.answer(text="Murojat uchun telefonlar:\n"\
    #                         "+998947405220  Komila\n"\
    #                         "+998947406220  Sarvinoz\n"\
    #                         "+998947407220  Diyora\n"\
    #                         "+998911357797  Sarvinoz\n"\
    #                         "@renuqabul2023\n"\
    #                         "@Renuadmin2\n"\
    #                         "@Renaissance7220\n"\
    #                         "@Renuadmin3")
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
