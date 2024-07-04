from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Основная клавиатура для обычных пользователей
user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Помощь')],
        [KeyboardButton(text='Зарегистрироваться', request_contact=True)]
    ],
    resize_keyboard=True
)

# Основная клавиатура для администраторов
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Помощь')],
        [KeyboardButton(text='Зарегистрироваться', request_contact=True)],
        [KeyboardButton(text='Список пользователей')],
        [KeyboardButton(text='Неотвеченные сообщения')]
    ],
    resize_keyboard=True
)


# Inline-клавиатура для админов
def create_admin_inline_keyboard(message_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Ответить', callback_data=f'reply_{message_id}')]
        ]
    )
    return keyboard
