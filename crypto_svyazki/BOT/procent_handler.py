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
   lang = await db.select_user(query.from_user.id)
   if not await db.get_status_subscribe(query.from_user.id): #Проверка на подписку
      await query.message.edit_text(await db.get_translated_text("<b>Чтобы полностью пользоваться арсеналом бота , надо активировать подписку</b>\n\n➖ Подписку активировать можно в личном кабинете",lang[0]))
   else:
      await query.message.edit_text((await db.get_translated_text("Для того чтобы мы могли присылать вам связки по торговле криптовалютой через арбитражный метод, вам необходимо вписать, в каком диапазоне процентов вы заинтересованы.\n\nПример: <code>0.{}-{}.{)}</code>", lang[0])).format(random.randint(1,9), random.randint(2,5), random.randint(1,9)))
      await state.set_state("set_arbitrj")

@dp.message_handler(state="set_arbitrj")
async def start(msg : types.Message, state: FSMContext):
   lang = await db.select_user(msg.from_user.id)
   try:
      if all(map(lambda x: isinstance(float(x), (int, float)), msg.text.split("-"))) and len(msg.text.split("-")) == 2:
         await db.update_procent_user(msg.from_user.id , msg.text)

         await msg.answer((await db.get_translated_text("🧮 <b>Диапазон процентов при арбитраже был изменен</b>\n<b>На</b> : от <code>{}</code> до <code>{}</code> %", lang[0])).format(*msg.text.split("-")))
      else:
         await msg.answer(await db.get_translated_text("<b>❗️Введите корректный диапозон чисел\n</b>Пример: 0.5-3.8", lang[0]))
   except Exception as E:
      await msg.answer(await db.get_translated_text("<b>❗️Введите корректный диапозон чисел\n</b>Пример: 0.5-3.8", lang[0]))

     