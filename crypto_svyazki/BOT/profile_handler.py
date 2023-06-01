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
from keyboards.profile_keyboard import get_button_profile
import random
#==================================================
from loader import bot, dp , db
#==================================================


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
""",reply_markup=await get_button_profile())




@dp.callback_query_handler(text_contains="addcrypto",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.set_state("add_adress")
    await query.message.answer("Введите свой крипто адресс <b>TRC-20 USDT</b>\n\nОн нужен для того чтобы получать выплаты за рефералов")


@dp.message_handler(text_contains="*",state="add_adress")
async def start(msg : types.Message, state: FSMContext):
   adress = msg.text
   await db.add_dress(msg.from_user.id,adress)