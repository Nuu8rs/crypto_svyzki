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
from logger import log
#==================================================


@dp.message_handler(commands=['start'],state="*")
async def start(msg : types.Message, state: FSMContext):
   await state.finish()
   lang = await db.select_user(msg.from_user.id)
   if await db.check_user(msg.from_user.id):
      await db.add_user(msg.from_user.id,msg.from_user.username)
   if not await db.get_status_subscribe(msg.from_user.id): #Проверка на подписку
      await msg.answer(await db.get_translated_text("<b>Чтобы полностью пользоваться арсеналом бота , надо активировать подписку</b>\n\n➖ Подписку активировать можно в личном кабинете", lang[0]))
   await bot.send_photo(msg.from_user.id , url_start_message , caption= (await db.get_translated_text("👋 Привествую  <b>{}</b>", lang[0])).format(msg.from_user.username),reply_markup=await start_keyboard())



@dp.message_handler(text_contains="👤Профиль",state="*")
async def start(msg : types.Message, state: FSMContext):
   try:
      await state.finish()
      lang = await db.select_user(msg.from_user.id)
      user_info       = await db.get_user_info(msg.from_user.id)
      stats_subscribe = await db.full_info_subscribe(msg.from_user.id)

      if "-" not in user_info[0]:
         diapazon = await db.get_translated_text("Не установлен", lang[0])
      else:
         diapazon = (await db.get_translated_text("""<code>{}</code> до <code>{}</code> %""", lang[0])).format(*user_info[0].split("-"))
      await msg.answer((await db.get_translated_text("""
   🔗 Профиль
   ├ <b>ID</b>: <code>{}</code>
   ├ <b>Tag</b>: @{}
   ├ <b>Диапазон арбитража</b>: {}
   └ <b>Дата регистрации</b>: <code>{}</code>

   🪢 Подписка
   ├ <b>Статус подписки</b>: {}
   └ <b>Действие подписки до</b>: <u>{}</u>
   """, lang[0])).format(msg.from_user.id, msg.from_user.username, diapazon, user_info[1], *stats_subscribe),reply_markup=await get_button_subscribe())
   except Exception as E:
      log.error(f"У пользователя : @{msg.from_user.username} произошла ошибка - {E}")
@dp.message_handler(text_contains="🖇Настройки",state="*")
async def start(msg : types.Message, state: FSMContext):
      await state.finish()
      lang = await db.select_user(msg.from_user.id)
      await msg.answer(await db.get_translated_text("""
   <b>⚙️ 
   Тут вы можете настроить процент арбитража под себя</b>
      """, lang[0]),reply_markup= await get_button_arb())
