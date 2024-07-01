import asyncio
from app.handlers import router
#from app.database import create_tables
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher


# Загрузка токена из .env файла
load_dotenv()
BOT_TOKEN = os.getenv('TG_TOKEN')

# Инициализация бота и диспетчера
async def main():
 #   await create_tables()  # Инициализация базы данных
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print('Exit')
