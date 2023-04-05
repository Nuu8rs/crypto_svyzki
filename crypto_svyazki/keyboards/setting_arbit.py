from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardMarkup , InlineKeyboardButton
from aiogram.dispatcher import FSMContext
async def get_button_arb():
   menu_arbitraj = InlineKeyboardMarkup(row_widht = 1)  
   sett_arbitraj = InlineKeyboardButton(f"⚒Настроить %", callback_data="arbit_procent")
   menu_arbitraj.add(sett_arbitraj)
   return menu_arbitraj