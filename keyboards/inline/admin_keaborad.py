import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

# Turli tugmalar uchun CallbackData-obyektlarni yaratib olamiz
application = CallbackData("contract", "contract_id", "action")

test=CallbackData("poll","question","action","value")
def make_test_callback_data(question,action,value):
    return test.new(
        question=question,action=action,value=value,
    )
def make_contract_callback_data(contract_id,action):
    return application.new(
        contract_id=contract_id,action=action
    )
def make_contract_keyboard(contract:str):
    makrkup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Qabul qilish",callback_data=make_contract_callback_data(
                    contract_id=contract,action="accept"
                )),
                InlineKeyboardButton("Arhivga otqazish",callback_data=make_contract_callback_data(
                    contract_id=contract,action="archive"
                ))
            ]
        ],
    )
    return makrkup
def make_resend_keyboard(contract:str):
    makrkup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Shartnomane boshqatan jo'natish",callback_data=make_contract_callback_data(
                    contract_id=contract,action="accept"
                )),
            ]
        ],
    )
    return makrkup
def make_archive_keyboard(contract:str):
    makrkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Qabul qilish", callback_data=make_contract_callback_data(
                    contract_id=contract, action="accept"
                )),
                InlineKeyboardButton("Bazadan ochirish", callback_data=make_contract_callback_data(
                    contract_id=contract, action="delete"
                ))
            ]
        ],
    )
    return makrkup



def make_test_keyboard(question_number:str):
    markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="A",callback_data=make_test_callback_data(
                    question=question_number,action="answer",value="A")),
                InlineKeyboardButton(text="B", callback_data=make_test_callback_data(
                    question=question_number, action="answer", value="B"))
            ],
            [
                InlineKeyboardButton(text="C", callback_data=make_test_callback_data(
                    question=question_number, action="answer", value="D")),
                InlineKeyboardButton(text="D", callback_data=make_test_callback_data(
                    question=question_number, action="answer", value="D"))
            ],
            [
                InlineKeyboardButton(text="Testni to'xtatish", callback_data=make_test_callback_data(
                    question=question_number, action="stop", value="")),
            ],

        ],
    )
    return markup

