from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.request import get_employee
from app.database.models import User

data = ("Коллега 1", "Коллега 2", "Коллега 3")

async def choose_college():
    ids = ['1', '2', '3']
    print(ids)
    keyboard = InlineKeyboardBuilder()
    for i in ids:
        keyboard.add(InlineKeyboardButton(text=i, url = f'tg://user?id={i}'))
    return keyboard.adjust(2).as_markup()

