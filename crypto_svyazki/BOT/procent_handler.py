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
import random
#==================================================
from loader import bot, dp , db
#==================================================

@dp.callback_query_handler(text_contains="arbit_procent",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   if not await db.get_status_subscribe(query.from_user.id): #Проверка на подписку
      await query.message.edit_text("<b>Чтобы полностью пользоваться арсеналом бота , надо активировать подписку</b>\n\n➖ Подписку активировать можно в личном кабинете")
   else:
      await query.message.edit_text(f"Для того чтобы мы могли присылать вам связки по торговле криптовалютой через арбитражный метод, вам необходимо вписать, в каком диапазоне процентов вы заинтересованы.\n\nПример: <code>0.{random.randint(1,9)}-{random.randint(2,5)}.{random.randint(1,9)}</code>")
      await state.set_state("set_arbitrj")

@dp.message_handler(state="set_arbitrj")
async def start(msg : types.Message, state: FSMContext):
   try:
      if all(map(lambda x: isinstance(float(x), (int, float)), msg.text.split("-"))) and len(msg.text.split("-")) == 2:
         await db.update_procent_user(msg.from_user.id , msg.text)

         await msg.answer(f"🧮 <b>Диапазон процентов при арбитраже был изменен</b>\n<b>На</b> : от <code>" +msg.text.split("-")[0]+"</code> до <code>"+msg.text.split("-")[1]+ "</code> %")
      else:
         await msg.answer("<b>❗️Введите корректный диапозон чисел\n</b>Пример: 0.5-3.8")
   except Exception as E:
      await msg.answer("<b>❗️Введите корректный диапозон чисел\n</b>Пример: 0.5-3.8")
     