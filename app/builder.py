from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.request import get_employee
from app.database.models import User

data = ("Коллега 1", "Коллега 2", "Коллега 3")

async def choose_college():
    list[User] = await get_list()
    keyboard = InlineKeyboardBuilder()
    for i in list:
        keyboard.add(InlineKeyboardButton(text= str(i), url = f'tg://user?id={i}'))
    return keyboard.adjust(2).as_markup()


async def get_list():
    list = await get_employee()
    print(list)
    return list
