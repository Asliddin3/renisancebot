from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS
from loader import db

class AdminFilter(BoundFilter):
    async def check(self, message:types.Message) -> bool:
        print(ADMINS)
        if message.from_user.id not in list(ADMINS):
            return False
        user=await db.get_user_state_by_telegram_id(message.from_user.id)
        state=user
        if ";" in state:
            return True
        return False

class AdminContentFilter(BoundFilter):
    async def check(self, message:types.Message) -> bool:
        if message.from_user.id not in list(ADMINS):
            return False
        user=await db.get_user_state_by_telegram_id(message.from_user.id)
        if ":" in user:
            return False
        state=user.split(";")
        if state[1]!="":
            if state[1] in ["all","accepted","archive","registered"]:
                return True
            return False
        return False


class AdminExelFilter(BoundFilter):
    async def check(self, message:types.Message) -> bool:
        user=await db.get_user_state_by_telegram_id(message.from_user.id)
        if message.from_user.id not in list(ADMINS):
            return False
        if ":" in user:
            return False
        state=user.split(";")
        if state[0]=="admin" and state[1]=="" and state[2]=="":
            return True
        return False