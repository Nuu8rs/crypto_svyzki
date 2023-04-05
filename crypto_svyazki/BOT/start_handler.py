import sys
sys.path.insert(0, '../CRYPTO_SVYZKI')

import ast
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import decode_payload
from aiogram.types import Message
#==================================================
from keyboards.start_keyboard import start_keyboard
from keyboards.buy_subscribe  import get_button_subscribe
from keyboards.setting_arbit  import get_button_arb
from loader import bot, dp , db
from config.utils import url_start_message
#==================================================


@dp.message_handler(commands=['start'],state="*")
async def start(msg : types.Message, state: FSMContext):
   await state.finish()
   if await db.check_user(msg.from_user.id):
      await db.add_user(msg.from_user.id,msg.from_user.username)
   if not await db.get_status_subscribe(msg.from_user.id): #Проверка на подписку
      await msg.answer("<b>Чтобы полностью пользоваться арсеналом бота , надо активировать подписку</b>\n\n➖ Подписку активировать можно в личном кабинете")
   await bot.send_photo(msg.from_user.id , url_start_message , caption= "<b>👋 Привествую  </b>"+msg.from_user.username,reply_markup=await start_keyboard())



@dp.message_handler(text_contains="👤Профиль",state="*")
async def start(msg : types.Message, state: FSMContext):
   await state.finish()
   user_info       = await db.get_user_info(msg.from_user.id)
   stats_subscribe = await db.full_info_subscribe(msg.from_user.id)

   if "-" not in user_info[0]:
      diapazon = "Не установлен"
   else:
      diapazon = f"""<code>{user_info[0].split("-")[0]}</code> до <code>{user_info[0].split("-")[1]}</code> %"""
   await msg.answer(f"""
🔗 Профиль
├ <b>ID</b>: <code>{msg.from_user.id}</code>
├ <b>Tag</b>: @{msg.from_user.username}
├ <b>Диапазон арбитража</b>: {diapazon}
└ <b>Дата регистрации</b>: <code>{user_info[1]}</code>

🪢 Подписка
├ <b>Статус подписки</b>: {stats_subscribe[0]}
└ <b>Действие подписки до</b>: <u>{stats_subscribe[1]}</u>
""",reply_markup=await get_button_subscribe())
   
@dp.message_handler(text_contains="🖇Настройки",state="*")
async def start(msg : types.Message, state: FSMContext):
   await state.finish()
   await msg.answer(f"""
<b>⚙️ 
Тут вы можете настроить процент арбитража под себя</b>
   """,reply_markup= await get_button_arb())
