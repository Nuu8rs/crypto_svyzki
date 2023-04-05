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
import qrcode
from io import BytesIO
import requests
import json
from PIL import Image
import time
from datetime import datetime, timedelta
#==================================================
from loader import bot, dp , db
from keyboards.buy_subscribe import get_prices , check_status_update_balance
from config.utils import adress , TRONGRID_API_URL , usdt_trc20_contract_address
#==================================================

@dp.callback_query_handler(text_contains="subs_open_button",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   await query.message.edit_text("<b>🧰 Тут вы можете активировать/продлить свою подписку</b>\n\n📕Подписка на <b>1 день</b> - <code>3 usdt</code>\n📗Подписка на <b>7 дней</b> - <code>7 usdt</code>\n📘Подписка на <b>31 день</b> - <code>30 usdt</code>",reply_markup= await get_prices())



@dp.callback_query_handler(text_contains="buy",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   await query.answer()
   photo = await get_qr_usdt()
   await bot.send_photo(query.from_user.id , photo=photo , caption=f"""➖ <b><u>Адрес</u></b> : <code>{adress}</code>\n\n<b><u>➖ Сумма пополнения</u></b> : {query.data.split(":")[-1]} USDT""",reply_markup=await check_status_update_balance())


async def get_qr_usdt():
   img = qrcode.make(f"tron:{adress}")
   stream = BytesIO()
   img.save(stream, format="PNG")
   qr_bytes = stream.getvalue()
   return qr_bytes



@dp.callback_query_handler(text_contains="check_opl",state="*")
async def add_otvet(query: CallbackQuery, state: FSMContext):
   result = await get_info_ca()
   #Сделать проверку через езерскан кошеля привязанного в utils и проверку добавить
   #status = await check_status_opl(query.data.split(":")[-1])
   # if status:
   #    if int( query.data.split(":")[-1] ) >= 3 and  int( query.data.split(":")[-1] ) < 7:

   #    if int( query.data.split(":")[-1] ) >= 7 and  int( query.data.split(":")[-1] ) < 30:

   #    await db.add_time_subscribe(query.from_user.id , query.data.split(":")[-1])

async def get_info_ca():
      amounts_to_check = [0.01, 7, 30]
      start_timestamp = int(time.time() * 1000) - 86400 * 1000  # Check transactions for the last 24 hours
      transactions =  get_transactions(start_timestamp)
      transfers =  get_usdt_trc20_transfers(transactions)
      found_amounts = []
      print(transfers)
      for transfer in transfers:
         if float(transfer["amount"]) in amounts_to_check:
               found_amounts.append(transfer["amount"])

      if found_amounts:
         response_text = f"Найдены пополнения на следующие суммы: {', '.join(map(str, found_amounts))} USDT."
      else:
         response_text = "Пополнений на указанные суммы не найдено."
      print(response_text)

def get_transactions(start_timestamp=0):
    time_lookback = datetime.utcnow() - timedelta(hours=5)
    url = f"{TRONGRID_API_URL}/v1/accounts/{adress}/transactions?min_timestamp={start_timestamp}&search_internal=false&limit=50"
    response = requests.get(url)
    return response.json()
def get_usdt_trc20_transfers(transactions):
    usdt_trc20_transfers = []
    for tx in transactions.get("data", []):
      contract_ret = tx.get("ret", [{}])[0].get("contractRet")
      if contract_ret != "SUCCESS":
         continue
      contract_data = tx.get("raw_data", {}).get("contract", [])[0].get("parameter", {}).get("value", {})
      try:
         usdt_trc20_transfers.append(
            {
                  "tx_id": tx["txID"],
                  "from": contract_data["owner_address"],
                  "amount": contract_data["amount"],
            }
         )
      except:
          continue
    return usdt_trc20_transfers
