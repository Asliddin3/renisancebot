from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_admin=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ariza topshirganlar"),
            KeyboardButton(text="Arhivdagilar")
        ],
        [
            KeyboardButton(text="Qabul bo'lganlar"),
            KeyboardButton(text="Elon qilish")
        ],[
            KeyboardButton(text="Excel yuklavolish"),
            KeyboardButton(text="Shartnoma idsi boicha qidirish")
        ],[
            KeyboardButton(text="Chiqish")
        ]
    ],
    resize_keyboard=True
)
notificationType=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Registraciyadan o'tganlarga"),
            KeyboardButton(text="Arhivdagilarga")
        ],
        [
            KeyboardButton(text="Hammaga jonatish"),
            KeyboardButton(text="Qabul bolganlarga")
        ],[

            KeyboardButton(text="🔙 Ortga")
        ]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙 Ortga")
        ]
    ],
    resize_keyboard=True
)