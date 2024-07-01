from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ChatAction
import app.keyboards as kb
from aiogram.filters import CommandStart

router = Router()



class Reg(StatesGroup):
    name = State()
    number = State()
    contact = State()
    user_id = State()
    chat_id = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Reg.name)  # Установка состояния Reg.name
    await message.answer(f'Привет! Для регистрации отправьте свой контакт, кнопка ниже', reply_markup=kb.login)

@router.message(F.contact)
async def handle_contact(message: Message, state: FSMContext):
    # Выводим данные контакта в терминал, но тут Вы уже сами решаете, как взаимодействовать с данными. Скорее всего Вам понадобитсья подключить базу данных, для того, чтобы сохранять их, но это не включено в данный вопрос :)
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
    if message.contact.user_id == message.from_user.id:
        await message.answer(f'Рады видеть тебя, {data['name']}!' , reply_markup=kb.main)
        await state.clear()


@router.message(F.text == 'Войти в аккаунт' )
async def login(message: Message, state: FSMContext):
    if Reg.name == None:
        await message.answer('Авторизация...' + Reg.name)
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
    await message.reply('Информация для инвесторов')


@router.message(F.text == 'Клиентам')
async def clients(message: Message):
    await message.reply('Информация для клиентов')


@router.message(F.text == 'Назад')
async def cmd_start(message: Message):
    await message.answer('И снова здравствуйте!', reply_markup=kb.main)


@router.message(F.text == 'Написать коллеге')
async def send_to_college(message: Message):
    await message.answer("Введите сообщение:", reply_markup= kb.message_confirm)


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
    await message.answer(f'Вам пришло сообщение от <a href={user_url}>{user_name}</a>', parse_mode='HTML')



@router.message(F.text == 'Отправить')
async def on_user_send(message: Message):
    message.answer('Сообщение  отправлено')


