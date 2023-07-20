from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ro'yxatdan o'tish"),
            KeyboardButton(text="Biz haqimizda")
        ],
    ],
    resize_keyboard=True,
)
lang=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="O'zbek"),
            KeyboardButton(text="Ruscha")
        ],
        [
            # KeyboardButton(text="Ingliz"),
            KeyboardButton(text="🔙 Ortga")
        ]
    ],resize_keyboard=True
)
testKey=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Imtihonni boshlash")
        ],
        [
            KeyboardButton(text="🔙 Ortga"),
            KeyboardButton(text="🏠 Bosh menu")
        ]
    ],resize_keyboard=True
)

format=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kunduzgi"),
            KeyboardButton(text="Kechgi")
        ],
        [
            KeyboardButton(text="Sirtqi")
        ],
        [
            KeyboardButton(text="🔙 Ortga"),
            KeyboardButton(text="🏠 Bosh menu")
        ]
    ],resize_keyboard=True
)

dtmKey=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ha"),
            KeyboardButton("Yoq")
        ],
        [
            KeyboardButton(text="🔙 Ortga"),
            KeyboardButton(text="🏠 Bosh menu")
        ]
    ],
    resize_keyboard=True
)
backKeyboard=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙 Ortga"),
            KeyboardButton(text="🏠 Bosh menu")
        ]
    ],resize_keyboard=True,
)

def make_fakultet_keyboard(fakultets: list[str]):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for val in fakultets:
        val=val[0]
        key = KeyboardButton(text=val)
        row.append(key)
        if len(row) == 2:
            markup.add(*row)  # Use add() to add multiple buttons to a row
            row = []
    if len(row) != 0:
        markup.add(*row)
        row = []
    row = [KeyboardButton("🔙 Ortga"), KeyboardButton("🏠 Bosh menu")]
    markup.add(*row)

    return markup


