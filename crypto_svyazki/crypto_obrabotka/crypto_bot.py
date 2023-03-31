import sys
sys.path.insert(0, '../CRYPTO_SVYZKI')

from config.utils import api_key,api_secret , bybit_api_key , bybit_api_secret , OKX_key , OKX_api_secter

from config.utils import prices

from datetime import datetime
import time
import requests
import hashlib
import json
import asyncio
#===========================================
from binance.client import Client    #Бинанс
from pybit import HTTP               #ByBit

client = Client(api_key=api_key, api_secret=api_secret)
http = HTTP()

#===========================================





async def get_all_token_binance():
    global client

    tickers = client.get_ticker()
    usdt_tokens = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')]

    for token in usdt_tokens:
        prices["binance"][token["symbol"].replace("USDT","").lower()] = (float(token["askPrice"]), float(token["bidPrice"]))
async def get_all_token_bybit():
    global HTTP
    results = http.best_bid_ask_price()
    for x in results.get("result"):
        if "USDT" in x["symbol"]:
            prices["bybit"][x["symbol"].replace("USDT","").lower()] = (float(x["askPrice"]), float(x["bidPrice"]))


async def get_all_token_OKX():
    params = {
        "instType": "SPOT",
        "quoteCcy": "USDT",
        "api_key": OKX_key
    }
    response = requests.get("https://www.okex.com/api/v5/market/tickers", params=params)

    data = response.json()
    for ticker in data["data"]:
        symbol = ticker["instId"]
        if symbol.split("-")[1] == "USDT":
            prices["okx"][symbol.replace("-USDT","").lower()] = (float(ticker["askPx"]), float(ticker["bidPx"]))

async def get_all_token_huobi():
    huobi_ticker_url = "https://api.huobi.pro/market/tickers"
    huobi_tickers = requests.get(huobi_ticker_url).json()["data"]
    for t in huobi_tickers:
        symbol = t["symbol"]
        if "usdt" in symbol:
            prices["huobi"][symbol.replace("usdt","").lower()] = (float(t["ask"]), float(t["bid"]))




async def waiting():
    await asyncio.wait([get_all_token_binance(), get_all_token_bybit(), get_all_token_OKX() , get_all_token_huobi()])
    for currency in prices["binance"]:
        if currency in prices["okx"] and currency in prices["huobi"] and currency in prices["bybit"]:
            buy_price_binance, sell_price_binance = prices["binance"][currency]
            buy_price_okx, sell_price_okx = prices["okx"][currency]
            buy_price_huobi, sell_price_huobi = prices["huobi"][currency]
            buy_price_bybit, sell_price_bybit = prices["bybit"][currency]
            
            # Находим максимальный sell_price и минимальный buy_price для нахождения процента
            max_sell_price = max(sell_price_binance, sell_price_okx, sell_price_huobi, sell_price_bybit)
            min_buy_price = min(buy_price_binance, buy_price_okx, buy_price_huobi, buy_price_bybit)
            
            # Считаем процент
            if max_sell_price > 0 and min_buy_price > 0:
                percent = ((max_sell_price - min_buy_price) / min_buy_price) * 100
                print(f"{currency} percent: {percent}")

asyncio.run(waiting())