import asyncio
from app.bot import router
#from app.database import create_tables
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
#from app.database.models import async_main
from app.database import create_table


# Загрузка токена из .env файла
load_dotenv()
BOT_TOKEN = os.getenv('TG_TOKEN')

# Инициализация бота и диспетчера
async def main():
 #   await create_tables()  # Инициализация базы данных
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher):

    await create_table()
    print('Starting up...')
async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
