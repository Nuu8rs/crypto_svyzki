import sys
sys.path.insert(0, '../CRYPTO_SVYZKI')

from binance.client import Client

from config.utils import api_key,api_secret
# Замените YOUR_API_KEY и YOUR_SECRET_KEY своими ключами API
client = Client(api_key=api_key, api_secret=api_secret)

# Получить все цены на токены на Binance
tickers = client.get_all_tickers()

# Распечатать список цен на токены
for ticker in tickers:
    print(ticker)