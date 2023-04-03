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
        if all(currency in prices[exchange] for exchange in prices):
            max_sell_price = max(prices[exchange][currency][1] for exchange in prices)
            min_buy_price = min(prices[exchange][currency][0] for exchange in prices)
            if min_buy_price > 0 and max_sell_price > 0:
                percent = ((max_sell_price - min_buy_price) / min_buy_price) * 100
                exchanges = [exchange for exchange in prices if prices[exchange][currency][0] == min_buy_price] + \
                            [exchange for exchange in prices if prices[exchange][currency][1] == max_sell_price]
                print(f"{currency}: Buy at {exchanges[0]}, sell at {exchanges[1]}, profit: {percent:.2f}%")


asyncio.run(waiting())