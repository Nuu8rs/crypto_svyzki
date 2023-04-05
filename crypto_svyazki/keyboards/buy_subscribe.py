from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardMarkup , InlineKeyboardButton
from aiogram.dispatcher import FSMContext
async def get_button_subscribe():
   menu_subscribe = InlineKeyboardMarkup(row_widht = 1)  

   buy_subscribe = InlineKeyboardButton(f"📍Активировать подписку", callback_data="subs_open_button")


   menu_subscribe.add(buy_subscribe)

   return menu_subscribe


async def get_prices():
   menu_subscribe = InlineKeyboardMarkup(row_widht = 1)  
   buy_subscribe_1 = InlineKeyboardButton(f"📕Активировать подписку на 1 день", callback_data="buy:1:3")
   buy_subscribe_2 = InlineKeyboardButton(f"📗Активировать подписку на 7 дней", callback_data="buy:10:7")
   buy_subscribe_3 = InlineKeyboardButton(f"📘Активировать подписку на 31 день", callback_data="buy:30:30")

   menu_subscribe.add(buy_subscribe_1).add(buy_subscribe_2).add(buy_subscribe_3)

   return menu_subscribe

async def check_status_update_balance():
   menu_subscribe = InlineKeyboardMarkup(row_widht = 1)  
   buy_subscribe_1 = InlineKeyboardButton(f"Проверить статус пополнения", callback_data="check_opl")

   menu_subscribe.add(buy_subscribe_1)

   return menu_subscribe