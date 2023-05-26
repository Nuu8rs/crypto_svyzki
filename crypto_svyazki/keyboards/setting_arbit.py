from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardMarkup , InlineKeyboardButton
from aiogram.dispatcher import FSMContext

import sys
sys.path.insert(0, '../CRYPTO_SVYZKI')
from loader import bot, dp , db

async def get_button_arb():
   menu_arbitraj = InlineKeyboardMarkup(row_widht = 1)  
   sett_arbitraj = InlineKeyboardButton(f"⚒ Настроить процент", callback_data="arbit_procent")
   sett_arbitraj_metod = InlineKeyboardButton(f"🪜 Метод поиска cвязок", callback_data="arbit_metod")
   sett_arbitraj_ban_tokens  = InlineKeyboardButton(f"🕳 Черный список токенов", callback_data="black_spisok")
   sett_arbitraj_ban_birj  = InlineKeyboardButton(f"🕳 Черный список бирж", callback_data="blackbirj")
   menu_arbitraj.add(sett_arbitraj).add(sett_arbitraj_metod).row(sett_arbitraj_ban_tokens,sett_arbitraj_ban_birj)
   return menu_arbitraj


async def change_metod(user_id):
   menu_arbitraj = InlineKeyboardMarkup(row_widht = 1)  
   sett_arbitraj_metod = InlineKeyboardButton(f"🔃 Сменить метод поиска", callback_data="arjange")
   menu_arbitraj.add(sett_arbitraj_metod)
   return menu_arbitraj

async def get_menu_black():
   menu_arbitraj = InlineKeyboardMarkup(row_widht = 1)  
   sett_1 = InlineKeyboardButton(f"➕ Добавить в черный список", callback_data="tokenban")
   sett_2 = InlineKeyboardButton(f"➖ Убрать с черного списка", callback_data="anban")
   menu_arbitraj.add(sett_1).add(sett_2)
   return menu_arbitraj

async def get_ban_token(user_id):
   texts = await db.get_ban_token(user_id)
   menu_arbitraj = InlineKeyboardMarkup(row_widht = 2)
   if not texts:
      return None
   for text in texts:
      sett_1 = InlineKeyboardButton(f"🔙 {text}", callback_data=f"unban:{text}") 
      menu_arbitraj.insert(sett_1)
   return menu_arbitraj

async def get_ban_birje(user_id):
   birje = await db.get_status_birje(user_id)
   menu_arbitraj = InlineKeyboardMarkup(row_widht = 3)
   arr_emdj = {"True":"✅","False":"❌"}
   for x in birje.split(","):
         text = f"""{x.split(':')[0]} {arr_emdj[x.split(':')[1]]}"""
         sett_1 = InlineKeyboardButton(f"{text}", callback_data=f"birjban:{x.split(':')[0]}") 
         menu_arbitraj.insert(sett_1)
   return menu_arbitraj