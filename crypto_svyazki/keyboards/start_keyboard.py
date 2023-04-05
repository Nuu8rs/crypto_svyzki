from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardMarkup , InlineKeyboardButton
from aiogram.dispatcher import FSMContext
async def start_keyboard():
    menu_users = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
    Pars           = KeyboardButton('👤Профиль')
    Settings_users = KeyboardButton('🖇Настройки')
    menu_users.add(Pars).row(Settings_users)

    return menu_users

