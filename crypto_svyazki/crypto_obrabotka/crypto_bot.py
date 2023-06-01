import sys
sys.path.insert(0, '../CRYPTO_SVYZKI')

from config.utils import api_key,api_secret , bybit_api_key ,  OKX_key , OKX_api_secter , kucoin_api_key, kucoin_api_secret, kucoin_api_pass
from config.utils import ban_token
from config.utils import prices
from datetime import datetime
import time
import requests
import hashlib
import json
import asyncio
import aiohttp
import aiomysql
from kucoin.client import Market, Trade
from loader import bot, dp , db
#===========================================
from binance.client import Client    #Бинанс
from pybit.unified_trading import HTTP         #ByBit
client = Client(api_key=api_key, api_secret=api_secret)
http = HTTP()
market_client = Market(url='https://api.kucoin.com')
kucoin_client = Trade(kucoin_api_key, kucoin_api_secret, kucoin_api_pass)

#===========================================





async def get_all_token_binance():
    global client

    tickers = client.get_ticker()
    usdt_tokens = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')]

    for token in usdt_tokens:
        if not any(token["symbol"].replace("USDT","").lower() in currency.lower() for currency in ban_token) and token["symbol"].replace("USDT","").lower()[-2:] not in ["3s","3l"] :
            prices["binance"][token["symbol"].replace("USDT","").lower()] = (float(token["askPrice"]), float(token["bidPrice"]))
async def get_all_token_bybit():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.crypto.com/v2/public/get-ticker") as response:
            tickers_data = await response.json()
            for ticker_info in tickers_data['result']["data"]:
                symbol = ticker_info['i']
                # Check the conditions
                if "USDT" in symbol and not any(symbol.replace("_USDT", "").lower() in currency.lower() for currency in ban_token) and symbol.replace("_USDT", "").lower()[-2:] not in ["3s", "3l"]:
                    # Add the best bid and ask prices to the prices dictionary
                    prices["bybit"][symbol.replace("_USDT", "").lower()] = (float(ticker_info['a']), float(ticker_info['b']))
async def get_all_token_kraken():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.kraken.com/0/public/Ticker") as response:
            data = await response.json()
            for market, ticker_data in data['result'].items():
                if market.endswith('USDT') and not any(market.replace("USDT","").lower() in currency.lower() for currency in ban_token) and market.replace("USDT","").lower()[-2:]not in ["3s","3l"]:
                    prices["kraken"][market.replace("USDT","").lower()] = (float(ticker_data['a'][0]), float(ticker_data['b'][0]))
            
async def get_all_token_OKX():
    params = {
        "instType": "SPOT",
        "quoteCcy": "USDT",
        "api_key": OKX_key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.okex.com/api/v5/market/tickers", params=params) as response:
            data = await response.json()
            for ticker in data["data"]:
                symbol = ticker["instId"]
                if symbol.split("-")[1] == "USDT" and not any(symbol.replace("-USDT","").lower() in currency.lower() for currency in ban_token) and symbol.replace("-USDT","").lower()[-2:]not in ["3s","3l"]:
                    prices["okx"][symbol.replace("-USDT","").lower()] = (float(ticker["askPx"]), float(ticker["bidPx"]))

async def get_all_token_huobi():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.huobi.pro/market/tickers") as response:
                data = await response.json()
                for t in data["data"]:
                        symbol = t["symbol"]
                        if "usdt" in symbol  and not any(symbol.replace("usdt","").lower() in currency.lower() for currency in ban_token) and symbol.replace("usdt","").lower()[-2:]not in ["3s","3l"]:
                            prices["huobi"][symbol.replace("usdt","").lower()] = (float(t["ask"]), float(t["bid"]))
    except:
        return await get_all_token_huobi

async def get_all_tokem_gate():
    all_tickers_url = "https://api.gate.io/api2/1/tickers"

    async with aiohttp.ClientSession() as session:
        async with session.get(all_tickers_url) as response:
            all_tickers = await response.json()
            usdt_pairs = {k: v for k, v in all_tickers.items() if k.endswith("_usdt")}
            usdt_pair_data = {}
            for symbol, ticker in usdt_pairs.items():    
                try:
                    
                    if not any(symbol.replace("_usdt","").lower() in currency.lower() for currency in ban_token) and symbol.replace("_usdt","").lower()[-2:]not in ["3s","3l"]:
                        prices["gate"][symbol.replace("_usdt","").lower()] = (float(ticker['lowestAsk']), float(ticker['highestBid']))
                except:
                    pass
            

async def get_all_token_kucoin():
    all_symbols = market_client.get_all_tickers()
    usdt_pairs = [symbol for symbol in all_symbols['ticker'] if symbol['symbolName'].endswith('USDT')]
    usdt_pair_data = {}
    for pair in usdt_pairs:
        try:
            symbol = pair['symbolName'].replace("-USDT","")
            if not any(symbol.lower() in currency.lower() for currency in ban_token)  and symbol.lower()[-2:]not in ["3s","3l"]:
                prices["kucoin"][symbol.lower()] = (float(pair['buy']), float(pair['sell']))
        except:
            pass

async def get_all_token_crypto():

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.crypto.com/v2/public/get-ticker") as response:
            all_tickers = await response.json()
            ticker = all_tickers["result"]["data"]
            for tiket in ticker:
                try:
                    symbol = tiket["i"]
                    if symbol.endswith("_USDT"):
                        if not any(symbol.replace("_USDT","").lower() in currency.lower() for currency in ban_token) and symbol.replace("_USDT","").lower()[-2:]not in ["3s","3l"]:
                            prices["crypto"][symbol.replace("_USDT","").lower()] = (float(tiket["a"]),float(tiket["b"]))
                except:
                    pass   
            

async def get_all_token_bitfinex():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api-pub.bitfinex.com/v2/tickers?symbols=ALL") as response:
            all_tickers = await response.json()
            usdt_pairs = [symbol for symbol in all_tickers if symbol[0].endswith("UST")]
            for pair in usdt_pairs:
                try:
                    symbol = pair[0][1:]
                    if not any(symbol.lower() in currency.lower() for currency in ban_token) and symbol.replace("UST","").lower()[-2:]not in ["3s","3l"]:
                        prices["bitfinex"][symbol.replace("UST","").replace(":","").lower()] = (float(pair[3]),float(pair[1]))
                except:
                    pass   

async def get_all_token_mexc():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.mexc.com/open/api/v2/market/ticker") as response:
            all_tickers = await response.json()
            all_tickers = all_tickers["data"]
            usdt_pairs = [market for market in all_tickers if market["symbol"].endswith("_USDT")]
            for pair in usdt_pairs:
                try:
                    symbol = pair["symbol"].replace("_USDT","").lower()
                    if not any(symbol.lower() in currency.lower() for currency in ban_token) and symbol.lower()[-2:]not in ["3s","3l"]:
                        prices["mexc"][symbol] = (float(pair["ask"]),float(pair["bid"]))
                except:
                    pass   


# async def get_all_token_hotbit():
#     async with aiohttp.ClientSession() as session:
#         async with session.get("https://api.hotbit.io/api/v1/allticker") as response:
#             response_text = await response.text()
#             markets = json.loads(response_text)
#             all_tickers = markets.get("ticker")
#             usdt_pairs = [market for market in all_tickers if market["symbol"].endswith("USDT")]
#             for pair in usdt_pairs:
#                 try:
#                     symbol = pair["symbol"].replace("_USDT","").lower()
#                     prices["hotbit"][symbol] = (float(pair["buy"]),float(pair["sell"]))
#                 except:
#                     pass   
            


async def get_all_token_exmo():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.exmo.com/v1.1/pair_settings") as response:
            markets = await response.json()

    usdt_pairs = [pair for pair in markets.keys() if pair.endswith("_USDT")]

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.exmo.com/v1.1/order_book?pair={','.join(usdt_pairs)}&limit=1") as response:
            tickers = await response.json()

    usdt_pair_data = {}
    for pair in usdt_pairs:
        symbol = pair.replace("_USDT","").lower()
        if not any(symbol.lower() in currency.lower() for currency in ban_token) and symbol.lower()[-2:]not in ["3s","3l"] :
            prices["exmo"][symbol] = (float(tickers[pair]['ask'][0][0]),float(tickers[pair]['bid'][0][0]))
    

async def get_all_token_poloniex():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://poloniex.com/public?command=returnTicker") as response:
            markets = await response.json()
            for pair, data in markets.items():
                try:
                    if pair.startswith("USDT"):
                        symbol = pair.replace("USDT_","").lower()
                        if not any(symbol.lower() in currency.lower() for currency in ban_token) and symbol.lower()[-2:]not in ["3s","3l"]:
                            prices["poloniex"][symbol] = (float(data['lowestAsk']),float(data['highestBid']))
                except:
                    pass
            

async def waiting():
    global prices
    while True:
        try:
            arr_tokens = []
    #       await asyncio.wait([get_all_token_binance(),get_all_tokem_gate(),get_all_token_crypto()])

            await asyncio.wait([get_all_token_binance(), get_all_token_bybit(), get_all_token_OKX() , get_all_token_huobi(),get_all_token_kraken(),get_all_tokem_gate(),get_all_token_kucoin(),get_all_token_crypto() , get_all_token_bitfinex(),get_all_token_mexc() , get_all_token_exmo() , get_all_token_poloniex()])
            for currency in set(prices["binance"]).union(prices["okx"]).union(prices["huobi"]).union(prices["bybit"]).union(prices["kraken"]).union(prices["kucoin"]).union(prices["gate"]).union(prices["crypto"]).union(prices["bitfinex"]).union(prices["mexc"]).union(prices["exmo"]).union(prices["poloniex"]):
                if sum(currency in prices[exchange] for exchange in prices) >= 2:
                    max_sell_price = max(prices[exchange][currency][1] for exchange in prices if currency in prices[exchange])
                    min_buy_price = min(prices[exchange][currency][0] for exchange in prices if currency in prices[exchange])

                    if min_buy_price > 0 and max_sell_price > 0:
                        percent = ((max_sell_price - min_buy_price) / min_buy_price) * 100
                        exchanges = [exchange for exchange in prices if currency in prices[exchange] and  prices[exchange][currency][0] == min_buy_price ] + \
                                    [exchange for exchange in prices if currency in prices[exchange] and prices[exchange][currency][1] == max_sell_price ]
                        
                        
                        if float(percent) >= 0 and exchanges[0] != exchanges[1]: 
                            arr_tokens.append({"token":currency,"one":f"{exchanges[0]}","two":f"{exchanges[1]}","profit":f"{percent:.2f}"})
            await send_inforamtion(arr_tokens)            
            prices = {
                "binance": {},
                "okx": {},
                "huobi": {},
                "bybit": {},
                "kraken" : {},
                "kucoin" : {},
                "gate"   : {},
                "crypto" : {},
                "bitfinex" : {},
                "mexc" : {},
                "exmo" : {},
                "poloniex": {},
                    }
        except Exception as E:
            print(E)
#"hotbit" : {},      

async def get_address_token(token,adress1,addres2):
    url_adress={"binance":"https://www.binance.com/en/trade/token_USDT?_from=markets","okx":"https://www.okx.com/ru/trade-spot/token-usdt","huobi":"https://www.huobi.com/ru-ru/exchange/token_usdt/","bybit":"https://www.bybit.com/trade/usdt/tokenUSDT","kraken":"https://futures.kraken.com/trade/futures/PF_tokenUSD",
                "kucoin" : "https://www.kucoin.com/ru/trade/token-USDT" , "gate" : "https://www.gate.io/ru/trade/token_USDT" , "crypto":"https://crypto.com/exchange/trade/token_USDT" , "bitfinex":"https://trading.bitfinex.com/t/token:UST?type=exchange","mexc":"https://www.mexc.com/ru-RU/exchange/token_USDT" , "exmo" : "https://exmo.me/trade/token_USDT",
                "poloniex" : "https://poloniex.com/trade/token_USDT/?type=spot"
                }
    token = token.upper()
    url_adrrss1 = url_adress[adress1].replace("token",token) 
    url_adrrss2 = url_adress[addres2].replace("token",token)

    if adress1 == "huobi":
        url_adrrss1 = url_adress[adress1].replace("token",token.lower()) 
    if addres2 == "huobi":
        url_adrrss1 = url_adress[adress1].replace("token",token.lower()) 
    text_link = f'<a href="{url_adrrss1}">Buy</a>|<a href="{url_adrrss2}">Sell</a>'
    return text_link

async def send_inforamtion(arr_tokens):
    list_users = await db.get_all_users_info()
    for user in list_users:
        id_user           = user[0]
        lang              = await db.select_user(id_user)
        arr_token_ban     = await db.get_ban_token(id_user)
        birje_status      = await db.get_status_birje(id_user)
        status_dict = {key: value for key, value in (status.split(":") for status in birje_status.split(","))}
        procent           = user[1]
        procent = "90-100"
        subscribe         = user[2]
        if "Подписка"  in subscribe :
            continue
        elif int(time.time()) >= int(subscribe):
            await db.delete_subscribe(id_user)
            await bot.send_message(id_user, await db.get_translated_text("‼️ <b>У вас закончилось время активной подписки</b> ‼️\n\nЧтобы <b>обновить подписку</b> , продлите ее в личном кабинете", lang[0]))
        elif int(time.time()) <= int(subscribe):
            text = ""
            for info in arr_tokens:
                try:
                    if float(info['profit']) >= float(procent.split("-")[0]) and float(info['profit']) <= float(procent.split("-")[-1]):
                        if not any(info['token'].upper() in x for x in arr_token_ban):
                            if status_dict.get(info['two']) != "False" and status_dict.get(info['one']) != "False":
                                emoji = "🟠" if float(info['profit']) < 1 else "🟢" if float(info['profit']) < 30 else "🔴"
                                text_url = await get_address_token(info['token'] , info['one'] , info['two'])
                                text += f"""{emoji} <code>{info['token'].upper()+"/USDT":10}</code> <code>{info['one']:7}</code>➡️ <code>{info['two']:7}</code> <code>{info['profit']:4}%</code>[{text_url}]\n"""
                                
                        # text += f"📈 Купить токен : <code>{info['token'].upper()}/USDT</code> на бирже <b><u>{info['one']}</u></b> И продать на бирже <b><u>{info['two']}</u></b> \n📍 Сумма арбитража: <b>{info['profit']}</b> % [{text_url}]\n\n"
                except Exception as E:
                    pass
            if text != "":
                arr_text = text.split("\n")
                n = 10
                result = ['\n'.join(arr_text[i:i+n]) for i in range(0, len(arr_text), n)]
                for texts in result:
                    if len(text) > 1:
                        await bot.send_message(id_user,(await db.get_translated_text("▫️ <b>Нашлись крипто связки</b> ▫️\n\n{}", lang[0])).format(texts),disable_web_page_preview=True)
                        await asyncio.sleep(300)

