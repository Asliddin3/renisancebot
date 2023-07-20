import asyncio

from aiogram import types
from aiogram.types import ContentType,InputMediaPhoto,InputMediaDocument,InputFile
from filters.admin_filter import AdminFilter,AdminContentFilter
from data.config import ADMINS
from loader import dp, db, bot
from keyboards.default.admin_keyboard import main_admin,back,notificationType
from keyboards.inline.admin_keaborad import make_contract_keyboard,make_archive_keyboard,application,make_resend_keyboard
from keyboards.default.start_keyboard import menu
from datetime import datetime
import pytz
import os
import pandas as pd
from generator import create_uchshartnoma,create_info,create_contract
timezone = pytz.timezone('Asia/Tashkent')

# @dp.message_handler(text="/exit",user_id=ADMINS)
# async def exit_admin_panel(message:types.Message):
#     await db.update_user_state(telegram_id=message.from_user.id,state="menu::::")
#     await message.answer(text="Bosh menu",reply_markup=menu)
uzbek_month_names = [
    "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr",
    "Oktabr", "Noyabr", "Dekabr"
]

@dp.callback_query_handler(application.filter(),AdminFilter(),user_id=ADMINS)
async def catch_admin_callback_data(call:types.CallbackQuery,callback_data:dict):
    contract_id=callback_data.get("contract_id")
    action=callback_data.get("action")
    if action=="accept":
        current_time = datetime.now(timezone)
        telegram_id=await db.get_user_telegram_id_by_contract(int(contract_id))
        await accept_student(message=call.message,contract_id=int(contract_id),created=current_time)
        await db.update_contract_state(id=int(contract_id),state="accepted")
        await db.update_contract_created_time(id=int(contract_id),created=current_time.date())
        await call.answer("Shartnoma jonatildi")
        malumotnoma=InputFile(f"/root/univer-bot/renisancebot/documents/{contract_id}/info.docx")
        shartnoma=InputFile(f"/root/univer-bot/renisancebot/documents/{contract_id}/shartnoma.docx")
        uchshartnoma=InputFile(f"/root/univer-bot/renisancebot/documents/{contract_id}/uchshartnoma.docx")
        await bot.send_message(text="Tabirklaymiz siz kabul kilindigiz.Sizning shartnomangiz")
        await bot.send_document(chat_id=telegram_id,document=malumotnoma,caption="Malumotnoma")
        await bot.send_document(chat_id=telegram_id,document=shartnoma,caption="Shartnoma")
        await bot.send_document(chat_id=telegram_id,document=uchshartnoma,caption="Uch tomonli")
    elif action=="archive":
        await db.update_contract_state(id=int(contract_id),state="archive")
        await call.answer("Arhivega solindi")
    elif action=="delete":
        await db.delete_contract(id=int(contract_id))
        await call.answer("Bazadan ochirildi")

info = {
    "name": "Asliddin Dehqonov ",
    "faculty": "moliya",
    "learn_type": "sirtqi",
    "id": "12421",
}


# Times={
#     'daytime':'Kunduzgi',
# 'evening':'Kechki',
# "distance":"Sirtqi"
# }
Lang={
'en': 'English',
'ru': 'Russian',
"uz":"Uzbek"
}
async def accept_student(message:types.Message,contract_id:int,created:datetime):
    full_info=await db.get_contract_full_info(contract_id)
    if full_info is None:
        await message.answer("Shartnoma topilmadi")
        return
    info_data={
        "id":full_info[0],
        "faculty":full_info[4],
        "learn_type":Times[full_info[5]],
        "name":full_info[1],
        "date":created.date()
    }
    create_info(info_data)
    finishYear=2027
    year=4
    if full_info[8]=="distance":
        finishYear=2028
        year=5
    data={
        "full_name":full_info[1],
        "id":str(full_info[0]),
        "price":str(full_info[6]),
        "price_text":full_info[7],
        "year":str(created.year),
        "day":str(created.day),
        "month":uzbek_month_names[created.month-1],
        "student_info":{
            "name": f"F.I.Sh.: {full_info[1]}",
            "address": full_info[9],
            "passport": f"Pasport ma’lumotlari: {full_info[10]}",
            "jshshir": f"JSHSHIR:  {full_info[11]}",
            "number": f"Telefon raqami: +{full_info[2]}\n+{full_info[3]}",
        },
        "contract_info":{
            "Ta’lim bosqichi:": "1-kurs",
            "Ta’lim shakli:": Lang[full_info[8]],
            "O‘qish muddati:":f"{year}-yil({finishYear})",
            "O‘quv kursi:": "1-bosqich, 1-semestrdan",
            "Ta’lim yo‘nalishi: ": full_info[4]
        }
    }
    create_contract(data)
    create_uchshartnoma(data)
    pass

@dp.message_handler(AdminContentFilter(),content_types=ContentType.ANY)
async def catch_admin_notification(message:types.Message):
    state=await db.get_user_state_by_telegram_id(message.from_user.id)
    state=state.split(";")
    if state[1] == "all":
        users = await db.select_all_users()
    else:
        users = await db.get_contract_users_by_state(state=state[1])
    if message.text == "🔙 Ortga":
        state[1] = "notification"
        state = ";".join(state)
        await db.update_user_state(telegram_id=message.from_user.id, state=state)
        await message.answer(text="Kimlarga elon jonatmoqchisiz", reply_markup=notificationType)
        return
    for user in users:
        user_id = user[0]
        if len(message.photo) != 0:
            await bot.send_photo(chat_id=user_id, caption=message.caption,
                                 photo=message.photo[0].file_id)
        elif message.video is not None:
            await bot.send_video(chat_id=user_id, caption=message.caption,
                                 photo=message.video.file_id)
        else:
            await bot.send_message(
                chat_id=user_id, text=message.text
            )
        await asyncio.sleep(0.05)

@dp.message_handler(AdminFilter(),user_id=ADMINS)
async def catch_admin_commands(message:types.Message):
    state=await db.get_user_state_by_telegram_id(message.from_user.id)
    state=state.split(";")
    if state[0]=="admin" and state[1]=="":
        text=message.text
        if text=="Chiqish":
            await message.answer("Bosh menu",reply_markup=menu)
            state="menu::::"
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            return
        elif text=="Ariza topshirganlar":
            contracts=await db.get_new_contracts()
            if len(contracts)==0:
                await message.answer("Yangi arizalar mavjud emas")
                return
            for contract in contracts:
                markup=make_contract_keyboard(contract[0])
                text=prepare_contract_data(contract)
                await message.answer(text=text,reply_markup=markup)
                passport=contract[10].split(":")
                passport_id,ptype=passport[1],passport[0]
                photo_ids=[]
                document_ids=[]
                if ptype=="photo":
                    photo_ids.append(passport_id)
                else:
                    document_ids.append(passport_id)
                diplom=contract[15].split(":")
                diplom_id, ptype = diplom[1], diplom[0]
                if ptype=="photo":
                    photo_ids.append(diplom_id)
                else:
                    document_ids.append(diplom_id)
                if len(photo_ids)!=0:
                    await message.answer_media_group(media=[InputMediaPhoto(media=photo_id) for photo_id in photo_ids])
                if len(document_ids)!=0:
                    await message.answer_media_group(media=[InputMediaDocument(media=photo_id) for photo_id in document_ids])
        elif text=="Arhivdagilar":
            contracts = await db.get_archived_contracts()
            if len(contracts)==0:
                await message.answer("Arhivda arizalar mavjud emas")
                return
            for contract in contracts:
                markup = make_archive_keyboard(contract[0])
                text = prepare_contract_data(contract)
                await message.answer(text=text, reply_markup=markup)
                photo = contract[10].split(":")
                photo_id, ptype = photo[1], photo[0]
                if ptype == "photo":
                    await message.answer_photo(photo=photo_id)
                else:
                    await message.answer_document(document=photo_id)
                # await message.answer_photo(photo=contract[10])
        elif text == "Qabul bo'lganlar":
            contracts=await db.get_accepted_contracts()
            if len(contracts)==0:
                await message.answer("Qabul bolgan arizalar mavjud emas")
                return
            for contract in contracts:
                text = prepare_contract_data(contract)
                markup=make_resend_keyboard(str(contract[0]))
                await message.answer(text=text,reply_markup=markup)
                photo = contract[10].split(":")
                photo_id, ptype = photo[1], photo[0]
                if ptype == "photo":
                    await message.answer_photo(photo=photo_id)
                else:
                    await message.answer_document(document=photo_id)
                # await message.answer_photo(photo=contract[10])
        elif text=="Excel yuklavolish":
            contracts = await db.get_students()
            df = pd.DataFrame(contracts, columns=['Shartnoma Idsi', 'F.I.SH',"Telefon raqami",
            "Ikkinchi telefon","Fakultet nomi","Ta'lim sharkli","Ta'lim Tili","Address","Passport",
            "JSHSHIR","DTM","Test natijasi","Shartnoma berilgan sana"])
            excel_file_path = 'talabalar.xlsx'  # Specify the file path where the Excel file will be saved
            df.to_excel(excel_file_path, index=False)
            with open(excel_file_path, 'rb') as file:
                await bot.send_document(message.from_user.id, file)
            os.remove(excel_file_path)

        elif text=="Elon qilish":
            state[1]="notification"
            state=";".join(state)
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            await message.answer(text="Kimlarga elon jonatmoqchisiz",reply_markup=notificationType)
        elif text=="Shartnoma idsi boicha qidirish":
            state[1]="student"
            state=";".join(state)
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            await message.answer(text="Shartnoma idsi kiriting",reply_markup=back)
    elif state[1]=="notification":
        if message.text=="🔙 Ortga":
            state[1]=""
            state=";".join(state)
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            await message.answer(text="Admin menu",reply_markup=main_admin)
        elif message.text in ["Registraciyadan o'tganlarga", "Arhivdagilarga", "Hammaga jonatish","Qabul bolganlarga"]:
            state[1] = notTypes[message.text]
            state=";".join(state)
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            await message.answer(text="Eloni kiriting",reply_markup=back)
        else:
            await message.answer("Hato amal kiritildi")
    elif state[1] in ["all","accepted","archive","registered"]:
        await message.answer("Bot nosoz ishlayapti")
    elif state[1]=="student":
        if message.text=="🔙 Ortga":
            state[1]=""
            state=";".join(state)
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            await message.answer(text="Admin menu",reply_markup=main_admin)
            return
        id=message.text
        contract =await db.get_contract_by_id(int(id))
        if len(contract)!=0:
            contract=contract[0]
            text=prepare_contract_data(contract)
            passport = contract[10].split(":")
            passport_id, ptype = passport[1], passport[0]
            # photo_ids = []
            # document_ids = []
            await message.answer(text=text)

            if ptype == "photo":
                # photo_ids.append(passport_id)
                await message.answer_photo(photo=passport_id)
            else:
                await message.answer_document(document=passport_id)
                # document_ids.append(passport_id)
            # print(contract[15])
            diplom = contract[15].split(":")
            print("diplom",diplom)
            diplom_id, ptype = diplom[1], diplom[0]
            if ptype == "photo":
                # photo_ids.append(diplom_id)
                await message.answer_photo(photo=diplom_id)
            else:
                # document_ids.append(diplom_id)
                await message.answer_document(document=diplom_id)
            # if len(photo_ids) != 0:
            #     print(photo_ids)
            #     await message.answer_media_group(media=[InputMediaPhoto(media=photo_id) for photo_id in photo_ids])
            # if len(document_ids) != 0:
            #     for document_id in document_ids:
            #         await message.answer_document(document=document_id)
        else:
            await message.answer("Bu id li shartnoma topilmadi")
        pass


notTypes={
    "Hammaga jonatish":"all",
    "Arhivdagilarga":"archive",
    "Registraciyadan o'tganlarga":"registered",
    "Qabul bolganlarga":"accepted"
}
Times = {
        'daytime':"Kunduzgi",
        "evening":'Kechgi' ,
        "distance":"Sirtqi"
}
langDic={
    "uz":"O'zbek",
    "ru":"Ruscha",
    "en":"Ingliz"
}

def prepare_contract_data(contract:list):
    res=f"<b>ID</b>:   {contract[0]}\n" \
        f"<b>F.I.SH</b>:         {contract[1]}\n" \
        f"<b>Telefon raqami</b>: {contract[2]}\n" \
        f"<b>Ikkinch telefon</b>:{contract[3]}\n" \
        f"<b>Fakultet nomi</b>:  {contract[4]}\n" \
        f"<b>Ta'lim shakli</b>:  {Times[contract[5]]}\n" \
        f"<b>Ta'lim tili</b>:    {langDic[contract[6]]}\n" \
        f"<b>Address</b>:        {contract[7]}\n" \
        f"<b>Passport IDsi</b>:  {contract[8]}\n" \
        f"<b>JSHSHIR</b>:        {contract[9]}\n"\
        f"<b>DTM</b>:        {contract[11]}\n" \
        f"<b>Test natijasi</b>:        {contract[12]}\n"
    if len(contract)>=14:
        res+=f"<b>Shartnoma jonatilgan sana</b>:        {contract[13]}\n"
        if len(contract)==15:
            res+=f"<a href='{contract[14]}'>Shartnoma linki</a>\n"
    return res


@dp.message_handler(text="/admin", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    state="admin;;"
    await db.update_user_state(telegram_id=message.from_user.id,state=state)
    await message.answer("Siz admin panelni ochdingiz",reply_markup=main_admin)
    # users = await db.select_all_users()
    # for user in users:
    #     # print(user[3])
    #     user_id = user[3]
    #     await bot.send_message(
    #         chat_id=user_id, text="Siz admin pan"
    #     )
    #     await asyncio.sleep(0.05)
