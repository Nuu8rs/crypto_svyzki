import requests

def get_binance_pairs():
    # Получаем список торговых пар
    response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
    symbols = response.json()["symbols"]

    # Фильтруем пары с USDT
    usdt_pairs = [symbol for symbol in symbols if symbol["quoteAsset"] == "USDT"]

    # Получаем информацию по тикерам
    response = requests.get("https://api.binance.com/api/v3/ticker/bookTicker")
    tickers = response.json()

    # Формируем словарь с информацией по тикерам
    ticker_dict = {ticker["symbol"]: ticker for ticker in tickers}

    # Получаем полные названия токенов с CoinGecko API
    response = requests.get("https://api.coingecko.com/api/v3/coins/list")
    coin_data = response.json()
    coin_name_dict = {coin["symbol"].upper(): coin["name"] for coin in coin_data}

    result = []

    for pair in usdt_pairs:
        symbol = pair["symbol"]
        base_asset_symbol = pair["baseAsset"]
        quote_asset_symbol = pair["quoteAsset"]

        if symbol in ticker_dict:
            base_asset_name = coin_name_dict.get(base_asset_symbol, base_asset_symbol)

            ask_price = ticker_dict[symbol]["askPrice"]
            bid_price = ticker_dict[symbol]["bidPrice"]
            result.append({
                "symbol": symbol,
                "baseAssetName": base_asset_name,
                "askPrice": ask_price,
                "bidPrice": bid_price
            })

    return result

usdt_pairs_with_prices = get_binance_pairs()
print(usdt_pairs_with_prices)