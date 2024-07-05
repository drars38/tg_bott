import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from app.database import add_user, add_message, get_unanswered_messages, respond_to_message, get_chat_id, get_message, \
    get_all_users
from app.keyboards import user_keyboard, admin_keyboard, create_admin_inline_keyboard

API_TOKEN = '7071804207:AAEjKYbRNlAZf23aMkz67qBr_cy1wkaNoQM'
ADMIN_USER_ID = [427368318]  # Список ID админов

logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()


class HelpMessage(StatesGroup):
    message_id = State()
    chat_id = State()
    message_send = State()


class AnswerMessage(StatesGroup):
    waiting_for_reply = State()


@router.message(Command("start"))
async def start(message: Message):
    user = message.from_user
    if user.id in ADMIN_USER_ID:
        keyboard = admin_keyboard
    else:
        keyboard = user_keyboard
    await message.reply(f'Привет! Вас приветствует служба поддержки Транснефть.', reply_markup=keyboard)




@router.message(Command("help"))
async def help_command(message: Message, state: FSMContext):
    await state.set_state(HelpMessage.message_send)
    await message.reply('Задайте ваш вопрос, и наша поддержка скоро свяжется с вами.')


@router.message(F.text == 'Помощь')
async def help_button(message: Message, state: FSMContext):
    await help_command(message, state)


@router.message(F.text == 'Список пользователей')
async def list_users_button(message: Message):
    if message.from_user.id in ADMIN_USER_ID:
        await list_users(message)
    else:
        await message.reply('У вас нет доступа к этой команде.')


@router.message(F.text == 'Неотвеченные сообщения')
async def list_unanswered_button(message: Message, state: FSMContext):
    if message.from_user.id in ADMIN_USER_ID:
        await list_unanswered(message, state)
    else:
        await message.reply('У вас нет доступа к этой команде.')


@router.message(Command("Список пользователей"))
async def list_users(message: Message):
    if message.from_user.id not in ADMIN_USER_ID:
        return
    users = await get_all_users()
    user_list = "\n".join([f'{user[1]}: {user[2]} {user[3]}' for user in users])
    await message.reply(f'Зарегистрированные пользователи:\n{user_list}')


@router.message(Command("Неотвеченные сообщения"))
async def list_unanswered(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_USER_ID:
        return
    unanswered = await get_unanswered_messages()
    if not unanswered:
        await message.reply('Нет необработанных сообщений.')
        return
    for msg in unanswered:
        keyboard = create_admin_inline_keyboard(msg[0])
        await message.reply(f'Сообщение от пользователя {msg[1]}:\n"{msg[2]}"', reply_markup=keyboard)


@router.callback_query(F.data.startswith('reply_'))
async def handle_reply_callback(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id not in ADMIN_USER_ID:
        await callback_query.answer('У вас нет доступа к этой функции.', show_alert=True)
        return
    message_id = callback_query.data.split('_')[1]
    await state.update_data(message_id=message_id)
    await state.set_state(AnswerMessage.waiting_for_reply)
    await callback_query.message.reply(f'Введите ответ на сообщение {message_id}.')
    await callback_query.answer()


@router.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    data = await state.get_data()
    current_state = await state.get_state()

    if current_state == AnswerMessage.waiting_for_reply.state:
        # Ответ администратора на сообщение пользователя
        if message.from_user.id in ADMIN_USER_ID:
            db_message_id = data['message_id']
            await respond_to_message(db_message_id, message.text)
            await message.reply(f'Ответ на сообщение {db_message_id} отправлен.')

            user_chat_id = await get_chat_id(db_message_id, 1)
            original_message = await get_message(db_message_id, 1)
            await bot.send_message(user_chat_id[0],
                                   f'❓ Ваше обращение:\n <b>{original_message[0]}</b>\n\n'
                                   f'🗣 Ответ от поддержки:\n <b><i>{message.text}</i></b>',
                                   parse_mode='HTML')
            await state.clear()
        else:
            print('Ошибка: текущее состояние - ожидание ответа, но сообщение не от администратора.')
    else:
        # Сообщение от пользователя
        if message.from_user.id not in ADMIN_USER_ID:
            user_message = message.text
            user = message.from_user
            db_message_id = await add_message(user.id, user_message)
            await state.update_data(message_id=db_message_id, chat_id=message.chat.id)
            await message.reply(f'Ваше сообщение: "{user_message}" получено. Ожидайте ответа.')
            await state.clear()
        else:
            print('Ошибка: сообщение от администратора, но текущее состояние не ожидание ответа.')

