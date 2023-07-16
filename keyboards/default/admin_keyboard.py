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
            KeyboardButton(text="Chiqish")
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