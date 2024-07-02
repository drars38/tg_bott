from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

data = ("Коллега 1", "Коллега 2", "Коллега 3")

def choose_college(user_id, chat_indo):
    keyboard = InlineKeyboardBuilder()
    for college in data:
        keyboard.add(InlineKeyboardButton(text=college, url = f'tg://user?id={user_id}'))
    return keyboard.adjust(2).as_markup()