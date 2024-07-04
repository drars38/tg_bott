from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
#from app.database.request import get_employee


data = ('Коллега 1','Коллега 2','Коллега 3')
async def choose_college():

    keyboard = InlineKeyboardBuilder()
    for i in data:
        keyboard.add(InlineKeyboardButton(text= str(i), url = f'tg://user?id={427368318}'))
    return keyboard.adjust(2).as_markup()





