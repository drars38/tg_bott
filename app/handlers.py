from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ChatAction
import app.keyboards as kb
from aiogram.filters import CommandStart
import app.builder as builder


router = Router()



class User(StatesGroup):
    name = State()
    number = State()
    contact = State()
    user_id = State()
    chat_id = State()



@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(User.name)  # Установка состояния User.name
    await message.answer(f'Привет! Для регистрации отправьте свой контакт, кнопка ниже', reply_markup=kb.login)

@router.message(F.contact)
async def handle_contact(message: Message, state: FSMContext):
    # Выводим данные контакта в терминал
    await state.update_data(name = message.contact.first_name)
    await state.update_data(number = message.contact.phone_number)
    await state.update_data(user_id = message.from_user.id)
    await state.update_data(chat_id = message.chat.id)
    data = await state.get_data()
    print('Новый контакт:')
    print('Имя: ' + data['name'])
    print('Номер телефона: ' + data['number'])
    print('ID пользователя: ' + str(data['user_id']))
    print('ID чата:' + str(data['chat_id']))
    data = await state.get_data()
    await message.answer(f'Рады видеть тебя, {data['name']}!', reply_markup=kb.main)
    if message.contact.user_id == message.from_user.id:
        await set_user(message.from_user.id, message.contact.first_name, message.contact.phone_number)
        await state.clear()



@router.message(F.text == 'Войти в аккаунт' )
async def login(message: Message, state: FSMContext):
    if User.name == None:
        await message.answer('Авторизация...' + User.name)
        #   в бд поиск аккаунта


# Обработка коллбэков для InlineKeyboardButton
@router.callback_query(F.data == 'callback_info')
async def info_callback(call: CallbackQuery):
    await call.message.answer('Тут большая история')


# Обработка текстовых сообщений для ReplyKeyboardButton
@router.message(F.text == 'О компании')
async def info(message: Message):
    await message.reply('Тут большая история', reply_markup=kb.settings)


@router.message(F.text == 'Задать вопрос')
async def development(message: Message):
    await message.answer('запрос', reply_markup=kb.inner_main)


@router.message(F.text == 'Инвесторам и акционерам')
async def investors(message: Message):
    await message.reply(str(await get_info('Информация для инвесторов')))


@router.message(F.text == 'Клиентам')
async def clients(message: Message):
    await message.reply(str(await get_info('Информация для клиентов')))


@router.message(F.text == 'Назад')
async def cmd_start(message: Message):
    await message.answer('И снова здравствуйте!', reply_markup=kb.main)


@router.message(F.text == 'Написать коллеге')
async def send_to_college(message: Message, bot: Bot):
    await message.answer("Выберите получателя:", reply_markup= await builder.choose_college())

@router.message(F.text == 'Тех. поддержка')
async def chat(message: Message, bot: Bot):
    help_user_id = message.from_user.id
    msg = message.answer(message.chat.id, 'Задайте вопрос', reply_markup=kb.message_confirm)








@router.message(F.text == 'Развлечения')
async def ai_chat(message: Message):
    await message.reply('Интеграция gamee')
@router.message(F.user_shared)
async def on_user_shared(message: Message):
    print(
        f"Request {message.user_shared.request_id}. "
        f"User ID: {message.user_shared.user_id}"
    )
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await message.bot.send_message(chat_id=message.user_shared.user_id, text='Тут сообщение от пользователя')

@router.message(F.text)
async def send_message(message: Message):
    user_name = str(message.from_user.full_name)
    user_url = str(message.from_user.url)
    await message.answer(f'Вам пришло сообщение от <a href="{user_url}">{user_name}</a>', parse_mode='HTML')


@router.message(F.data.startswith('send_to_'))
async def inp_message(callback: CallbackQuery):
    await callback.message.answer('Ваша корзина пуста.')

@router.message(F.text == 'Отправить')
async def on_user_send(message: Message):
    message.answer('Сообщение  отправлено')


