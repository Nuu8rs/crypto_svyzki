

import asyncio
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB_requests.sql import DateBase
bot = Bot(
    token="6141520620:AAHtdAwtt6-sYbn2IKgpBjISjuZJhh6kI1k",
    parse_mode=types.ParseMode.HTML
)
storage = MemoryStorage()
dp = Dispatcher(
        bot=bot,
        storage=storage,
    )
db = DateBase()
import crypto_obrabotka.crypto_bot , BOT.start_handler , BOT.procent_handler , BOT.subscribe_handler , BOT.settings_handler