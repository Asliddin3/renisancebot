import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.start_keyboard import menu
from loader import dp, db, bot
import  os
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
    text="Hurmatli talabalar universitet tanlashda qiynalayapsizmi ?\n"\
    "Qaysi Nodavlat taʼlim muassasalari diplomi tan olinadi ?\n"\
    "Litsenizyasi haqiqiymi  yoʻqmi ? Bu joyda oʻqisam keyin pullarimga kuyib qolmaymani ? shu kabi savollar sizni qiynayaptimi ?  Unda Nodavlat taʼlim muassasalariga litseniziya beruvchi vakolatli organ Oliy taʼlim fan va Innovatsiyalar vazirligi ishonch raqami 1006 yoki call markazi  712306464 ga qoʻngʻiroq qiling\n\n"\
    "https://stat.edu.uz/Univer-list.php\n"\
    "quyidagi havolada Oliy taʼlm vazirligi rasmiy saytida roʻyxati koʻrsatilgan litsenziyaga ega xususiy oliygohlar bilan tanishishingiz mumkin\n"
    path="/home/asliddin/PycharmProjects/renaissance/mukammal-bot-paid"
    photo1=f"./photo1.jpg"
    photo2=f"./photo2.jpg"
    if os.path.exists(photo1) and os.path.exists(photo2):
        media_group = [
            types.InputMediaPhoto(media=open(photo1, 'rb'),caption=text),
            types.InputMediaPhoto(media=open(photo2, 'rb'))
        ]
        await message.answer_media_group(media=media_group)
    text="Eng kerakli va zamonaviy kasblarni IIIU'da egallang!\n\n"\
    "📌 Bizning yo'nalishlar:\n"\
    "▫️ Boshlang'ich ta'lim;\n"\
    "▫️ Amaliy psixologiya;\n"\
    "▫️ Kompyuter ilmi va dasturlash texnologiyalari;\n"\
    "▫️ Maktabgacha ta'lim;\n"\
    "▫️ Filologiya va tillarni o'qitish;\n"\
    "▫️ Buxgalteriya va audit;\n"\
    "▫️ Moliya va moliyaviy texnologiyalar;\n"\
    "▫️ Iqtisodiyot.\n"\
    "✅ Ta'lim sifati kafolatlanadi:\n"\
    "Tajribali o'qituvchilarimizning 80% qismi ilmiy darajaga ega va ular xorij universitetlarida malaka oshirishadi.\n\n"\
    "✅ To'lov va moddiy ko'mak:\n"\
    "Talabalar oylik stipendiya bilan ta'minlanadi. Shartnoma to'lovi uchun ta'lim kreditini rasmiylashtirish imkoni mavjud.\n"\
    "✅ Onlayn imtihon:\n"\
    "Test sinovidan o'tish uchun hech qayerga borishingizga hojat yo'q. DTM imtihonidan 56.7 ball to'plaganlar esa imtihonsiz qabul qilinadi"
    photo1="./hand.jpg"
    with open(photo1, 'rb') as photo_file:
        await bot.send_photo(message.from_user.id, photo_file, caption=text)
    await message.answer_location(longitude=69.21678571163685, latitude=41.23966763877322,reply_markup=menu)
    # await message.answer_photo(photo=contract_id)
