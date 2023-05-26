from aiogram.utils import executor
from loader import bot, dp , db
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from crypto_obrabotka.crypto_bot import waiting
import asyncio
from logger import log
async def create(dispatcher: Dispatcher):
    asyncio.create_task(waiting())
    await db.create()

# test test

if __name__ == '__main__':
    log.info("Bot started")
    log.info("DataBase started")
    executor.start_polling(dp,on_startup=create)