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
from keyboards.setting_arbit import get_menu_black
import random
#==================================================
from loader import bot, dp , db
#==================================================

@dp.callback_query_handler(text_contains="arbit_metod",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   await query.answer()
   metod_find_user = await db.get_user_metod(query.from_user.id)

#    0 - 1 🟠 
# 1 - 30 🟢 
# 30 - n🟡
   arr_metod = {"M":"Межд биржевая торговля","V":"Внутри биржевая торговля"}
   await query.message.edit_text(f"⚖️ Ваш текущий метод поиска крипто связок - <b>{arr_metod[metod_find_user]}</b>\n\n<b>📥 Межд биржевая торговля</b> - тогда  в бот будет приходить крипто-связки <b><u>между</u></b> бирж\n\n<b>📤 Внутри биржевая торговля</b> - тогда в бот будет приходить крипто-связки <b><u>вунтри</u></b> биржи которую вы выберите",reply_markup=await change_metod(query.from_user.id))



   
@dp.callback_query_handler(text_contains="arjange",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   await query.answer()
   await db.change_metod(query.from_user.id)
   metod_find_user = await db.get_user_metod(query.from_user.id)

#    0 - 1 🟠 
# 1 - 30 🟢 
# 30 - n🟡
   arr_metod = {"M":"Межд биржевая торговля","V":"Внутри биржевая торговля"}
   await query.message.edit_text(f"⚖️ Ваш текущий метод поиска крипто связок - <b>{arr_metod[metod_find_user]}</b>\n\n<b>📥 Межд биржевая торговля</b> - тогда  в бот будет приходить крипто-связки <b><u>между</u></b> бирж\n\n<b>📤 Внутри биржевая торговля</b> - тогда в бот будет приходить крипто-связки <b><u>вунтри</u></b> биржи которую вы выберите",reply_markup=await change_metod(query.from_user.id))



   
@dp.callback_query_handler(text_contains="black_spisok",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   await query.message.edit_text("💾 <b>Выбирете действие</b>",reply_markup=await get_menu_black())

@dp.callback_query_handler(text_contains="tokenban",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   await query.message.edit_text("<b>Напишите название токена и с данным токеном у вас не будет крипто связок</b>")
   await state.set_state("addban_token")


@dp.message_handler(state="addban_token")
async def start(msg : types.Message, state: FSMContext):
   try:
      await db.add_ban_token(msg.from_user.id,msg.text)
      await msg.answer(f"Токен : {msg.text} был успешно внесен в черный список ✅")
   except Exception as E:
      print(E)
