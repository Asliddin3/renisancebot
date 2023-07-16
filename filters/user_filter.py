from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import db

class UserFilter(BoundFilter):
    async def check(self, message:types.Message) -> bool:
        user=await db.get_user_state_by_telegram_id(message.from_user.id)
        state=user
        if ":" in state:
            return True
        return False