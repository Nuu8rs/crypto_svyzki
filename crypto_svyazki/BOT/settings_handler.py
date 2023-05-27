import sys
sys.path.insert(0, '../CRYPTO_SVYZKI')
from keyboards.setting_arbit  import change_metod
import ast
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from aiogram.types import Message
from keyboards.setting_arbit import get_menu_black , get_ban_token , get_ban_birje
import random
#==================================================
from loader import bot, dp , db
#==================================================

@dp.callback_query_handler(text_contains="arbit_metod",state="*")
async def arbit_metod(query: CallbackQuery, state: FSMContext):
   await query.answer()
   lang = await db.select_user(query.from_user.id)
   metod_find_user = await db.get_user_metod(query.from_user.id)
   arr_metod = {"M":await db.get_translated_text("Межд биржевая торговля", lang[0]),"V":await db.get_translated_text("Внутри биржевая торговля", lang[0])}
   await query.message.edit_text((await db.get_translated_text("⚖️ Ваш текущий метод поиска крипто связок - <b>{}</b>\n\n<b>📥 Межд биржевая торговля</b> - тогда  в бот будет приходить крипто-связки <b><u>между</u></b> бирж\n\n<b>📤 Внутри биржевая торговля</b> - тогда в бот будет приходить крипто-связки <b><u>вунтри</u></b> биржи которую вы выберите", lang[0])).format(arr_metod[metod_find_user]),reply_markup=await change_metod(query.from_user.id))

@dp.callback_query_handler(text_contains="arjange",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   await db.change_metod(query.from_user.id)
   await arbit_metod(query, state)
   
@dp.callback_query_handler(text_contains="black_spisok",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   lang = await db.select_user(query.from_user.id)
   await query.message.edit_text(await db.get_translated_text("💾 <b>Выбирете действие</b>", lang[0]), reply_markup=await get_menu_black())

@dp.callback_query_handler(text_contains="tokenban",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   lang = await db.select_user(query.from_user.id)
   await query.answer()
   await query.message.answer(await db.get_translated_text("<b>Напишите название токена и с данным токеном у вас не будет крипто связок c <u>данным токеном</u></b>\n\n<b>Вы можете нажать на токен в связке и скопировать ее \n<u>Пробелы уберет бот</u></b>", lang[0]))
   await state.set_state("addban_token")

@dp.message_handler(state="addban_token")
async def start(msg : types.Message, state: FSMContext):
   lang = await db.select_user(msg.from_user.id)
   try:
      try:
         ban_token = msg.text.split("/")[0]
      except:
         ban_token = msg.text
      await db.add_ban_token(msg.from_user.id,ban_token)
      await msg.answer((await db.get_translated_text("""Токен : <code>{}</code> был успешно внесен в черный список ✅""", lang[0])).format(msg.text.upper().replace(" ","")))
   except Exception as E:
      print(E)

@dp.callback_query_handler(text_contains="anban",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   lang = await db.select_user(query.from_user.id)
   await query.answer()
   await query.message.answer(await db.get_translated_text("📍 Выберите <b>токен</b> , который хотите убрать с черного списка", lang[0]),reply_markup= await get_ban_token(query.from_user.id))

@dp.callback_query_handler(text_contains="unban",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   lang = await db.select_user(query.from_user.id)
   await query.answer()
   name_token = query.data.split(":")[1]
   await db.return_token(query.from_user.id , name_token)
   await query.message.edit_reply_markup(reply_markup=await get_ban_token(query.from_user.id))
   await query.message.answer((await db.get_translated_text("Токен <code>{}</code> был успешно удален с чёрного списка ✅", lang[0])).format(name_token))

@dp.callback_query_handler(text_contains="blackbirj",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   lang = await db.select_user(query.from_user.id)
   await query.message.edit_text(await db.get_translated_text("Меню настроек", lang[0]),reply_markup=await get_ban_birje(query.from_user.id))

@dp.callback_query_handler(text_contains="birjban",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   await db.edit_ban_birje(query.from_user.id,query.data.split(":")[1])
   await query.message.edit_reply_markup(reply_markup=await get_ban_birje(query.from_user.id))