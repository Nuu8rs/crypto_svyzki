from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardMarkup , InlineKeyboardButton
from aiogram.dispatcher import FSMContext



async def get_button_profile():
   menu_subscribe = InlineKeyboardMarkup(row_widht = 1)  

   buy_subscribe = InlineKeyboardButton(f"📍Активировать подписку", callback_data="subs_open_button")
   add_adress = InlineKeyboardButton(f"🪙Привязать крипто кошелек", callback_data="addcrypto")


   menu_subscribe.add(buy_subscribe).add(add_adress)

   return menu_subscribe