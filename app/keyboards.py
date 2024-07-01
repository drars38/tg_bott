from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Основная клавиатура
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Написать коллеге')],
    [KeyboardButton(text='О компании'), KeyboardButton(text='Задать вопрос')],
    [KeyboardButton(text='Инвесторам и акционерам'), KeyboardButton(text='Клиентам')],
    [KeyboardButton(text='Войти в аккаунт', request_contact=True)]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню.')

# Клавиатура для выбора получателя
async def get_recipient_keyboard():
    cars = ['Коллега 1', 'Коллега 2', 'Коллега 3']  # Замените на реальные данные или данные из БД

    keyboard = InlineKeyboardMarkup()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, callback_data=f"send_to_{car.replace(' ', '_')}"))

    return keyboard

# Клавиатура для внутреннего меню
inner_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Тех. поддержка'), KeyboardButton(text='Развлечения')],
    [KeyboardButton(text='Написать коллеге')],
    [KeyboardButton(text='Назад')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню.')

# Клавиатура подтверждения отправки сообщения
message_confirm = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить сообщение")],
    [KeyboardButton(text='Назад')]
], input_field_placeholder='Выберите пункт меню.')

# Inline клавиатура для настроек
settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ознакомиться', url='https://example.com')],
])

login = ReplyKeyboardMarkup(

    keyboard=[
        [KeyboardButton(text='Отправить контакт', request_contact=True)]
    ]

)
