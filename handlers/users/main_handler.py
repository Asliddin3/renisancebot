from loader import dp,db
from aiogram.types import ContentType,Message,CallbackQuery,ReplyKeyboardRemove
from keyboards.default.start_keyboard import lang,format,menu,make_fakultet_keyboard,backKeyboard,testKey
from keyboards.inline.menu_keyboards import make_test_keyboard,test

import re
from handlers.users.start import photo_id,jshshr_id

"""
States
state:lan:time:fakultet:

univer
lan

"""

langDic={
    "O'zbek":"uz",
    "Ruscha":"ru",
}
backDic={

    "lang":{
        "key":menu,
        "state":"menu",
        "text":"Assalomu alaykum, Xush kelibsiz. Universitetga ro'yxatdan o'tish uchun `Ro'yxatdan o'tish` tugmasini bosing"
    },
    "format":{
        "key":lang,
        "state":"lang",
        "text":"Iltimos ta'lim tilini tanlang"
    },
    "fakultet":{
        "key":format,
        "state":"format",
        "text":"Iltimos ta'lim shaklini tanlang"
    },
    "full_name":{
        "key":backKeyboard,
        "state":"fakultet",
        "text":"Yo'nalishni tanlang."
    },
    "phone":{
        "key":backKeyboard,
        "state":"full_name",
        "text":"Iltimos talabaning toliq F.I.SH kiriting "
    },
    "extra_phone":{
        "key":backKeyboard,
        "state":"phone",
        "text":"Iltimos talabaning telefon raqamini kiriting"
    },
    "passport":{
        "key":backKeyboard,
        "state":"extra_phone",
        "text":"Iltimos qoshimcha telefon raqam kiriting"
    },
    "JSHSHIR":{
        "key":backKeyboard,
        "state":"passport",
        "text":"Iltimos talabani passport raqamini yuboring"
    },
    "address":{
        "key":backKeyboard,
        "state":"JSHSHIR",
        "text":"Iltimos talabani JSHSHIR ni kiriting"
    },
    "photo":{
        "key":backKeyboard,
        "state":"address",
        "text":"Iltimos yashash joyingizni kiriting passportdagi"
    },
    "test":{
        "key":backKeyboard,
        "state":"photo",
        "text":"Talabaning passport rasmini kiriting"
    }
}


Times = {
         'Kunduzgi':'daytime',
        'Kechgi':'evening' ,
        "Sirtqi":"distance"
}

#
# @dp.message_handler(content_types=ContentType.VIDEO)
# async def catch_video(message:Message):
#     video_id=message.video.file_id
#     print(video_id)
#     await message.answer_video(video_id)

# @dp.message_handler(content_types=ContentType.LOCATION)
# async def get_location(message:Message):
#     await message.answer(text=f"long {message.location.longitude} lat {message.location.latitude}")

# @dp.message_handler(content_types=ContentType.PHOTO)
# async def catch_passport_photo(message:Message):
#     await message.answer(message.photo[-1].file_id)

@dp.message_handler(content_types=ContentType.PHOTO)
async def catch_passport_photo(message:Message):
    photo_id=message.photo[-1].file_id
    user = await db.get_user_state_by_telegram_id(message.from_user.id)
    state=user
    state = state.split(":")
    if state[0]!="photo":
        await message.answer("Hato amal kiritildi")
        return
    photo_id=f"photo:{photo_id}"

    await db.update_user_photo(message.from_user.id,photo_id=str(photo_id))
    state[0]="test"
    state=":".join(state)
    await db.update_user_state(telegram_id=message.from_user.id,state=state)
    await message.answer("Imtihonni boshlash uchun `Imtihonni boshlash` tugmasini bosing.",reply_markup=testKey)
@dp.message_handler(content_types=ContentType.DOCUMENT)
async def catch_passport_photo(message:Message):
    photo_id=message.document.file_id
    user = await db.get_user_state_by_telegram_id(message.from_user.id)
    state=user
    state = state.split(":")
    if state[0]!="photo":
        await message.answer("Hato amal kiritildi")
        return
    photo_id=f"document:{photo_id}"
    await db.update_user_photo(message.from_user.id,photo_id=str(photo_id))
    state[0]="test"
    state=":".join(state)
    await db.update_user_state(telegram_id=message.from_user.id,state=state)
    await message.answer("Imtihonni boshlash uchun `Imtihonni boshlash` tugmasini bosing.",reply_markup=testKey)



@dp.callback_query_handler(test.filter())
async def catch_answers(call:CallbackQuery,callback_data:dict):
    user = await  db.get_user_state_by_telegram_id(call.from_user.id)
    state=user
    state = state.split(":")
    question=callback_data.get("question")
    action=callback_data.get("action")
    value=callback_data.get("value")
    if state[0]!="exam":
        return
    number=None
    answer=""
    new_question=""
    if question != "":
        res = await db.get_question_with_answer(int(question))
        answer = res[0]
        new_question=res[1]
        number = res[2]
    if action == "stop":
        state[0]="test"
        state=":".join(state)
        await call.message.delete()
        await call.message.answer("Test tohtatildi",reply_markup=testKey)
        await db.delete_user_result(telegram_id=call.from_user.id)
        await db.update_user_state(telegram_id=call.from_user.id,state=state)
        return
    else:
        if answer==value:
            await db.increment_user_result(telegram_id=call.from_user.id)
            await call.answer("Javobingiz to'gri")
        else:
            await call.answer("Javobingiz noto'gri")
    if number!=None:
        markup=make_test_keyboard(str(number))
        await call.message.edit_text(text=new_question,reply_markup=markup)
    else:
        result=await db.get_user_result(call.from_user.id)
        state[0]="menu"
        await db.create_user_contract(telegram_id=call.from_user.id,
                                      fakultet_id=int(state[3]),result=result)
        state=":".join(state)
        await db.update_user_state(telegram_id=call.from_user.id,state=state)
        await call.message.delete()
        await call.message.answer(text=f"Togri topilgan javoblar soni {result}",)
        await call.message.answer(text="Malumotlaringiz jonatildi."
                                       "Natijalaringiz korib chiqilgandan kiyin shartnomani jonatamiz.",reply_markup=menu)





@dp.message_handler(content_types=ContentType.TEXT)
async def main_handler(message:Message):
    user=await db.get_user_state_by_telegram_id(message.from_user.id)
    state=user
    state=state.split(":")
    print(state)
    if state[0]=="menu":
        if message.text=="Ro'yxatdan o'tish":
            state[0]="lang"
            await message.answer("Iltimos ta'lim tilini tanlang.",reply_markup=lang)
        elif message.text=="Biz haqimizda":
            await message.answer_photo(photo=photo_id)
            await message.answer_location(longitude=69.210325,latitude=41.19043)
            await message.answer(f"<a href=\"https://t.me/renuadmisson/15\">✅Universitet haqida</a>\n"\
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
                "1 mlrdlik grant",reply_markup=menu, disable_web_page_preview=True)
    elif message.text=="🔙 Ortga":
        if state[0]=="full_name":
            state[0] = "fakultet"
            fakultets = await db.get_fakultets(language=state[1], time=state[2])
            fakultetKey = make_fakultet_keyboard(fakultets)
            await message.answer("Yo'nalishni tanlang.", reply_markup=fakultetKey)
        elif state[0]=="exam":
            await message.answer("Hato amal kirtildi")
            return
        else:
            backAns = backDic[state[0]]
            state[0]=backAns["state"]
            await message.answer(text=backAns["text"],reply_markup=backAns["key"])
    elif message.text=="🏠 Bosh menu":
        state[0]="menu"
        await message.answer(text="Assalomu alaykum, Xush kelibsiz. Universitetga ro'yxatdan o'tish uchun `Ro'yxatdan o'tish` tugmasini bosing",
                             reply_markup=menu)
    elif message.text in ["O'zbek","Ruscha","Ingliz"] and state[0]=="lang":
        state[0]="format"
        state[1]=langDic[message.text]
        await message.answer("Iltimos ta'lim shaklini tanlang.",reply_markup=format)
    elif message.text in ["Kunduzgi","Kechgi","Sirtqi"] and state[0]=="format":
        state[0]="fakultet"
        state[2]=Times[message.text]
        fakultets=await db.get_fakultets(language=state[1],time=Times[message.text])
        print(fakultets)
        if len(fakultets)==0:
            await message.answer("Bu ta'lim shakli boicha fakultet mavjud emas",reply_markup=format)
            return
        fakultetKey=make_fakultet_keyboard(fakultets)
        await message.answer("Yo'nalishni tanlang.",reply_markup=fakultetKey)
    elif state[0]=="fakultet":
        fakultet_id=await db.get_fakultet_id_by_name(message.text)
        if fakultet_id is None:
            await message.answer("Hato amal kiritildi")
            return
        state[0]="full_name"
        state[3]=str(fakultet_id[0])
        await message.answer("Iltimos talabaning toliq F.I.SH kiriting ", reply_markup=backKeyboard)
    elif state[0]=="full_name":
        if message.text.isdigit():
            await message.answer("F.I.SH hato kiritildi iltimos qaytadan kiriting")
            return
        await db.update_user_real_name(telegram_id=message.from_user.id,real_name=message.text)
        await message.answer("Iltimos talabaning telefon raqamini shu formata kiriting +998991112233",reply_markup=backKeyboard)
        state[0]="phone"
    elif state[0]=="phone":
        phone_number_pattern = re.compile(r'^\+998\d{9}$')
        if not phone_number_pattern.match(message.text):
            await message.answer("Telefon raqam hato kitildi iltimos shu formata kiriting +998901112233")
            return
        phone=message.text.replace("+","")
        tel = await db.get_contract_by_telefone(phone)
        if tel is not None:
            await message.answer("Bu nomerga contract tuzilib bolingan")
            return
        count=await db.check_for_phone_exists(phone)
        if count!=0:
            await message.answer("Bu telefon raqamga contract tuzilgan")
            return
        await message.answer("Iltimos qoshimcha telefon raqamni shu formata kiriting  +998901112233",reply_markup=backKeyboard)
        state[0]="extra_phone"
        await db.update_user_phone(message.from_user.id,phone)
    elif state[0]=="extra_phone":
        phone_number_pattern = re.compile(r'^\+998\d{9}$')
        if not phone_number_pattern.match(message.text):
            await message.answer("Telefon raqam hato kitildi iltimos shu formata kiriting +998901112233")
            return
        exists_phone=await db.get_user_phone_by_telegram_id(message.from_user.id)
        phone = message.text.replace("+", "")
        if exists_phone==phone:
            await message.answer("Iltimos boshqa telefon raqam kiriting bu telefon raqam kiritilgan")
            return
        await message.answer("Iltimos talabani passport raqamini yuboring  AB1231212", reply_markup=backKeyboard)
        state[0] = "passport"
        await db.update_user_extra_phone(message.from_user.id, phone)
    elif state[0]=="passport":
        passport_id_pattern = re.compile(r'^[A-Z]{2}\d{7}$')
        if not passport_id_pattern.match(message.text):
            await message.answer("Passport raqami hato kiritildi iltimos shu formata kiriting AB1234567")
            return
        text=message.text.upper()
        count = await db.check_for_phone_exists(text)
        if count != 0:
            await message.answer("Bu passport id raqamga contract tuzilgan")
            return
        await db.update_user_passport(telegram_id=message.from_user.id,passport=text)
        state[0]="JSHSHIR"
        await message.answer("Iltimos talabani JSHSHIR ni kiriting ",reply_markup=backKeyboard)
        await message.answer_photo(photo=jshshr_id)
        # await message.answer_photo()
    elif state[0] =="JSHSHIR":
        pattern =re.compile(r'^\d{14}')
        if not pattern.match(message.text):
            await message.answer("JSHSHIR hato kiritildi")
            return
        await db.update_user_jshshir(telegram_id=message.from_user.id,jshshir=message.text)
        state[0]="address"
        await message.answer(text="Iltimos yashash joyingizni kiriting passportdagi misol:"
                                  "Toshkent shahar Yakasaroy tumani Shota Rustaveli Kochasi 87 dom 99 honadon",reply_markup=backKeyboard)
    elif state[0]=="address":
        await db.update_user_address(message.from_user.id,message.text)
        state[0]="photo"
        await message.answer(text="Talabaning passport yoki id kartasini rasmini jonating",reply_markup=backKeyboard)
    elif state[0]=="test" and "Imtihonni boshlash":
        keyboard=make_test_keyboard("1")
        question=await db.get_test(1)
        if question=="":
            await message.answer("Testlar hali qoshilmadi")
            return
        await message.answer(text="Test boshlandi",reply_markup=ReplyKeyboardRemove())
        await message.answer(text=question,reply_markup=keyboard)
        state[0]="exam"
        await db.delete_user_result(telegram_id=message.from_user.id)
        # await db.update_user_status(message.from_user.id,"registered")
    else:
        await message.answer("Notogri amal bajarildi")
        return
    state=":".join(state)
    await db.update_user_state(message.from_user.id,state)


test={
    1:{
        "question":"1-Savol."\
                    "XIX asr o‘rtalarida xonliklar chorvadorlardan olingan soliq turini aniqlang?"\
                    "A. alg‘ut"\
                    "B. zakot"\
                    "C. salg‘ut"\
                    "D. kafsan,",
        "answer":"A"
    },
    2:{
        "question":"Test2?",
        "answer":"A"
    }
}

