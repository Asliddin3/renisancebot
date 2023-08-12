import asyncio
import time

import aiogram
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
from generator import create_uchtamonlama,create_info,create_contract
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
        if telegram_id is None:
            await call.message.answer("Bu id lis shartnoma mavjud emas")
            return
        await accept_student(message=call.message,contract_id=int(contract_id),created=current_time)
        await db.update_contract_state(id=int(contract_id),state="accepted")
        await db.update_contract_created_time(id=int(contract_id),created=current_time.date())
        await bot.send_message(chat_id=telegram_id,text="✅Tabriklaymiz siz Renaissance Universtyga talabalikka qabul qilindingiz !!!")
        malumotnoma=InputFile(f"/root/univer-bot/renisancebot/documents/{contract_id}/malumotnoma.pdf")
        shartnoma=InputFile(f"/root/univer-bot/renisancebot/documents/{contract_id}/shartnoma.pdf")
        uchtamonlama=InputFile(f"/root/univer-bot/renisancebot/documents/{contract_id}/uchtamonlama.pdf")
        await bot.send_document(chat_id=telegram_id,document=malumotnoma,caption="Ma'lumotnoma")
        await bot.send_document(chat_id=telegram_id,document=shartnoma,caption="Shartnoma")
        await bot.send_document(chat_id=telegram_id,document=uchtamonlama,caption="Uch tomonli")
        await call.answer("Shartnoma jo'natildi")

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
'en': 'Ingliz',
'ru': 'Rus tili',
"uz":"O'zbek"
}

async def accept_student(message:types.Message,contract_id:int,created:datetime):
    full_info=await db.get_contract_full_info(contract_id)
    if full_info is None:
        await message.answer("Shartnoma topilmadi")
        return
    id=2000+full_info[0]

    info_data={
        "id":f"01-04/{id}",
        "path":full_info[0],
        "faculty":full_info[4],
        "learn_type":Times[full_info[5]],
        "name":full_info[1],
        "date":created.strftime("%d.%m.%Y")
    }
    create_info(info_data)
    finishYear=2027
    year=4
    if full_info[5]=="distance":
        finishYear=2028
        year=5
    summa=full_info[6]/1000_000
    summa=int(summa)
    data={
        "full_name":full_info[1],
        "id":f"01-04/{id}",
        "path":full_info[0],
        "price":f"{summa} 000 000 ",
        "price_text":f"({full_info[7]})",
        "year":str(created.year),
        "day":str(created.day),
        "month":uzbek_month_names[created.month-1],
        "student_info":{
            "name": f"F.I.Sh.: {full_info[1]}",
            "address": f"Yashash manzili: {full_info[9]}",
            "passport": f"Pasport ma’lumotlari: {full_info[10]}",
            "jshshir": f"JSHSHIR:{full_info[11]}",
            "number": f"Telefon raqami: +{full_info[2]}\n+{full_info[3]}",
        },
        "contract_info":{
            "Ta’lim bosqichi:": "Bakalavr",
            "Ta’lim shakli:": Times[full_info[5]],
            "O‘qish muddati:":f"{year}-yil({finishYear})",
            "O‘quv kursi:": "1-bosqich",
            "Ta’lim yo‘nalishi:": f"{full_info[4]}",
            "Ta’lim tili:": langDic[full_info[8]],
        }
    }
    create_contract(data)
    create_uchtamonlama(data)

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
        await message.answer(text="Kimlarga elon jo'natmoqchisiz", reply_markup=notificationType)
        return
    sendMap={}
    for user in users:
        user_id = user[0]
        if sendMap.get(user_id):
            continue
        try:
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
            await asyncio.sleep(1)
            sendMap[user_id]=True
            print("message sended")
        except aiogram.utils.exceptions.BotBlocked:
            print("message blocked")
        except aiogram.utils.exceptions.UserDeactivated:
            print("user diactiveted")
        except:
            print("get any error")
    # except aiogram.utils.ex

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
                await asyncio.sleep(0.5)
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
                await asyncio.sleep(0.5)
        elif text=="Arhivdagilar":
            contracts = await db.get_archived_contracts()
            if len(contracts)==0:
                await message.answer("Arhivda arizalar mavjud emas")
                return
            for contract in contracts:
                markup = make_archive_keyboard(contract[0])
                text = prepare_contract_data(contract)
                await message.answer(text=text, reply_markup=markup)
                await asyncio.sleep(0.5)
                photo = contract[10].split(":")
                photo_id, ptype = photo[1], photo[0]
                if ptype == "photo":
                    await message.answer_photo(photo=photo_id)
                else:
                    await message.answer_document(document=photo_id)
                await asyncio.sleep(1)
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
                await asyncio.sleep(0.5)
                photo = contract[10].split(":")
                photo_id, ptype = photo[1], photo[0]
                if ptype == "photo":
                    await message.answer_photo(photo=photo_id)
                else:
                    await message.answer_document(document=photo_id)
                await asyncio.sleep(0.5)
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
            contracts = await db.get_fakultets_data()
            print(contracts)
            df = pd.DataFrame(contracts, columns=['Nome', 'Tili', "Ta'lim turi",
                                                  "Summa", "summa text"])
            excel_file_path = 'fakultet.xlsx'  # Specify the file path where the Excel file will be saved
            df.to_excel(excel_file_path, index=False)
            with open(excel_file_path, 'rb') as file:
                await bot.send_document(message.from_user.id, file)
            os.remove(excel_file_path)
        elif text=="Elon qilish":
            state[1]="notification"
            state=";".join(state)
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            await message.answer(text="Kimlarga elon jo'natmoqchisiz",reply_markup=notificationType)
        elif text=="Shartnoma idsi boicha qidirish":
            state[1]="student"
            state=";".join(state)
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            await message.answer(text="Shartnoma idsi kiriting",reply_markup=back)
        elif  text=="Shartnomani hammaga bo'shqatan jo'natish":
            contracts=await db.get_accepted_contracts_for_resend()
            for contract in contracts:
                contract_id=contract[0]
                telegram_id=contract[2]
                current_time=contract[1]
                # await accept_student(message,contract[0],current_time)
                try:
                    await accept_student(message=message, contract_id=int(contract_id), created=current_time)
                # await db.update_contract_state(id=int(contract_id), state="accepted")
                # await db.update_contract_created_time(id=int(contract_id), created=current_time.date())
                # await bot.send_message(chat_id=telegram_id,text="✅Tabriklaymiz siz Renaissance Universtyga talabalikka qabul qilindingiz !!!")
                    malumotnoma = InputFile(f"/root/univer-bot/renisancebot/documents/{contract_id}/malumotnoma.pdf")
                    shartnoma = InputFile(f"/root/univer-bot/renisancebot/documents/{contract_id}/shartnoma.pdf")
                    uchtamonlama = InputFile(f"/root/univer-bot/renisancebot/documents/{contract_id}/uchtamonlama.pdf")
                    await bot.send_document(chat_id=telegram_id, document=malumotnoma, caption="Ma'lumotnoma")
                    await bot.send_document(chat_id=telegram_id, document=shartnoma, caption="Shartnoma")
                    await bot.send_document(chat_id=telegram_id, document=uchtamonlama, caption="Uch tomonli")
                    await message.answer(text=f"Shartnoma jo'natildi idsi:{contract_id}")
                    time.sleep(1.5)
                except Exception as ex:
                    print("got error ",ex)
    elif state[1]=="notification":
        if message.text=="🔙 Ortga":
            state[1]=""
            state=";".join(state)
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            await message.answer(text="Admin menu",reply_markup=main_admin)
        elif message.text in ["Registraciyadan o'tganlarga", "Arhivdagilarga", "Hammaga jo'natish","Qabul bolganlarga"]:
            state[1] = notTypes[message.text]
            state=";".join(state)
            await db.update_user_state(telegram_id=message.from_user.id,state=state)
            await message.answer(text="Eloni kiriting",reply_markup=back)
        else:
            await message.answer("Xato amal kiritildi")
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
            markup=make_resend_keyboard(str(contract[0]))
            passport = contract[10].split(":")
            passport_id, ptype = passport[1], passport[0]
            await message.answer(text=text,reply_markup=markup)

            if ptype == "photo":
                # photo_ids.append(passport_id)
                await message.answer_photo(photo=passport_id)
            else:
                await message.answer_document(document=passport_id)
                # document_ids.append(passport_id)
            # print(contract[15])
            diplom = contract[15].split(":")
            diplom_id, ptype = diplom[1], diplom[0]
            if ptype == "photo":
                # photo_ids.append(diplom_id)
                await message.answer_photo(photo=diplom_id)
            else:
                # document_ids.append(diplom_id)
                await message.answer_document(document=diplom_id)

        else:
            await message.answer("Bu id li shartnoma topilmadi")
        pass


notTypes={
    "Hammaga jo'natish":"all",
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
    "ru":"Rus tili",
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
        res+=f"<b>Shartnoma jo'natilgan sana</b>:        {contract[13]}\n"
        enpoint="http://78.40.219.247:8000"
        res += f"<a href='{enpoint}/info/{contract[0]}'>Ma'lumotnoma</a>\n"
        res += f"<a href='{enpoint}/contract/{contract[0]}'>Shartnoma</a>\n"
        res += f"<a href='{enpoint}/document/{contract[0]}'>Uchtomonli Shartnoma</a>\n"
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
