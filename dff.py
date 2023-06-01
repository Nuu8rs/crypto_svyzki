from binance.client import Client
import asyncio
import binance.client
import re
# Insert your API keys
api_key = "nTfCKRwFem4nLTeDisMrZelsxrgKeQYyXlP0rKeaiY05giJOyT5zTiEYWiqtEEA7"
api_secret = "NLTGPyxp2dR3wA1zxqXcv3BZKuQRSmjqKukxws7uFrwsl6Be8v090rBdtHFi3ngJ"
currencies_all = ['PROS', 'ASTR', 'HARD', 'EGLD', 'ALCX', 'XAF', 'VIDT', 'WBTC', 'GALA', 'DREP', 'DKK', 'WIN', 'DAI', 'VET', 'PROM', 'FILUP', '1INCHDOWN', 'MKR', 'OSMO', 'SDG', 'MTLX', 'PAX', 'TWT', 'DOGE', 'DGB', 'MLN', 'DOT', 'NZD', 'FTM', 'ONG', 'BCHUP', 'XMR', 'CHF', 'BCH', 'TROY', 'ORN', 'MAGIC', 'ARS', 'UNFI', 'BAR', 'BCHA', 'IDEX', 'MXN', 'HIFI', 'FARM', 'IOST', 'ZEC', 'SAR', 'XNO', 'SXPDOWN', 'KNCL', 'XLMUP', 'JASMY', 'TWD', 'GLM', 'CHZ', 'LRC', 'ANKR', 'TRXOLD', 'FILDOWN', '1INCHUP', 'CTSI', 'MINA', 'LAZIO', 'SOL', 'ALGO', 'BEL', 'PKR', 'PIVX', 'UAH', 'T', 'DF', 'SPELL', 'INJ', 'CLP', 'ICX', 'SUSHI', 'GNS', 'AAVEUP', 'HFT', 'MA', 'PUNDIX', 'DIA', 'UYU', 'XRPUP', 'AGLD', 'IOTX', 'TFUEL', 'STMX', 'PARA', 'IMX', 'XEM', 'WING', 'RVN', 'BNX', 'BND', 'FIO', 'HOOK', 'AXS', 'ADADOWN', 'SRM', 'MBOX', 'ACA', 'FLR', 'CVC', 'BCHDOWN', 'YFIDOWN', 'MBL', 'OG', 'BGN', 'QKC', 'BNBDOWN', 'OM', 'LTCUP', 'ARDR', 'WNXM', 'RLC', 'EVX', 'AED', 'BTTC', 
'WETH', 'TVK', 'COTI', 'LIT', 'REEF', 'STPT', 'YFI', 'KWD', 'HIVE', 'SUI', 'KHR', 'SSV', 'TJS', 'NKN', 'JOD', 'KLAY', 'RAD', 'BNT', 'REQ', 'RCN', 'FET', 'CTK', 'XLM', 'SHIB', 'FXS', 'ALICE', 'MDX', 'NULS', 'SXP', 'WSOL', 'RNDR', 'KZT', 'MNT', 'PGALA', 'YFII', 'ENS', 'C98', 'GAS', 'DAR', 'TRB', 'SKL', 'WBNB', 'ACH', 'AERGO', 'ZAR', 'STEEM', 'BAKE', 'BOND', 'PEPE', 'SUN', 'EGP', 'BURGER', 'KEYFI', 'MC', 'SOLO', 'NOK', 'RAY', 'BADGER', 'NFT', 'PERL', 'DASH', 'TKO', 'ETC', 'YGG', 'PHP', 'YFIUP', 'CAN', 'TCT', 'LINKDOWN', 'EOSDOWN', 'QLC', 'PORTO', 'NVT', 'NEO', 'AR', 'BIFI', 'ZRX', 'WOO', 'FORTH', 'MASK', 'UFT', 'ID', 'SUSHIDOWN', 'FIL', 'UMA', 'RDNT', 'SYN', 'BTCDOWN', 'API3', 'AUD', 'BYN', 'FLM', 'LSK', 'DUSK', 'ALPACA', 'MOVR', 'GHST', 'HBAR', 'CHESS', 'ACM', 'TLM', 'DYDX', 'PLN', 'HRK', 'FIS', 'QUICK', 'BGBP', 'LINA', 'BLZ', 'XLMDOWN', 'BTTOLD', 'GMX', 'FIRO', 'ASR', 'RPL', 'BNC', 'XTZ', 'IOTA', 'EOS', 'ETH', 'DOP', 'BTCUP', 'AST', 'PNT', 'DZD', 'ETHW', 'LTO', 'QTUM', 'MOB', 'STG', 'FLOW', 'CHR', 'HIGH', 'JOE', 'XRP', 'ICP', 'XOF', 'NEXO', 'ZIL', 'DOTDOWN', 'KES', 'GHS', 'LEVER', 'QAR', 'CAD', 'PSG', 'VAI', 'FUN', 'VOXEL', 'RIF', 'AGIX', 'ATA', 'HOT', 
'OCEAN', 'SFP', 'REI', 'RON', 'DOCK', 'CLV', 'GYEN', 'ENJ', 'NMR', 'MDT', 'TRU', 'TRX', 'GRT', 'KP3R', 'KEY', 'GNO', 'DATA', 'ETB', 'KAVA', 'GMT', 'LTCDOWN', 'EDU', 'BAND', 'LINKUP', 'APE', 'TZS', 'ARPA', 'BHD', 'PLA', 'FLUX', 'ADA', 
'CELR', 'ATOM', 'LQTY', 'FIDA', 'GAL', 'PEN', 'AUDIO', 'ADAUP', 'WBETH', 'COP', 'KGS', 'WRX', 'CITY', 'UGX', 'MMK', 'VRT', 'TMT', 'EFI', 'BCX', 'KNC', 'IDRT', 'COMP', 'GFT', 'GRTDOWN', 'BETH', 'GTC', 'PHA', 'SYS', 'WAVES', 'KDA', 'SUPER', 'CZK', 'USDC', 'AUTO', 'BICO', 'GEL', 'TOMO', 'BETA', 'XRPDOWN', 'UNIDOWN', 'BIDR', 'QI', 'SEK', 'SAND', 'BTC', 'CFX', 'WAN', 'ALPHA', 'STRAX', 'AAVE', 'AUCTION', 'BSW', 'OAX', 'UNIUP', 'TRXUP', 'MTL', 'AFN', 'XEC', 'PYR', 'MULTI', 'DEXE', 'SNT', 'HUF', 'GBP', 'BNB', 'UTK', 'QNT', 'PERP', 'CKB', 'HKD', 'AMP', 'SANTOS', 'TND', 'LTC', 'SXPUP', 'SUSHIUP', 'USDT', 'USTC', 'SCRT', 'SLP', 'WTC', 'LOOKS', 'LUNA', 'COCOS', 'XVG', 'CVP', 'ELF', 'JUV', 'BUSD', 'DENT', 
'CAKE', 'DOTUP', 'LPT', 'POLYX', 'EPS', 'GRTUP', 'OMG', 'AMD', 'ATM', 'LBA', 'ARB', 'OMR', 'FLOKI', 'PHB', 'CREAM', 'NGN', 'RDNTOLD', 'COS', 'AVA', 'SBTC', 'FTT', 'EOSUP', 'LYD', 'FOR', 'JST', 'RSR', 'AAVEDOWN', 'ROSE', 'ALPINE', 'TORN', 'OP', 'LDO', 'LOKA', 'WAXP', 'DODO', 'POWR', 'MANA', 'ERN', 'THETA', 'LINK', 'ONT', 'PEOPLE', 'VITE', 'ADX', 'ILV', 'LAK', 'RARE', 'VIB', 'AKRO', 'CELO', 'APT', 'VND', 'USDP', 'PAXG', 'ZEN', 'TRY', 'JEX', 'FRONT', 'TUSD', 'ETHUP', 'IRIS', 'UZS', 'SC', 'RUNE', 'SNM', 'CTXC', 'LOOM', 'ARK', 'BAL', 'BNBUP', 'EUR', 'STX', 'BAT', 'XTZUP', 'JPY', 'IDR', 'UNI', 'BTS', 'EPX', 'GLMR', 'ANT', '1INCH', 'OGN', 'LUNC', 'ONE', 'NEAR', 'VGX', 'VTHO', 'BRL', 'STORJ', 'AVAX', 
'REN', 'MATIC', 'OOKI', 'BDOT', 'OXT', 'XVS', 'DEGO', 'ETHDOWN', 'KSM', 'POLS', 'USD', 'SNX', 'INR', 'CRV', 'XTZDOWN', 'NEBL', 'RUB', 'AMB', 'KMD', 'DCR', 'TRXDOWN', 'POND', 'CVX', 'IQ']
# Create a Binance client instance
stable = ["USDT","TUSD","BUSD"]
client = Client(api_key, api_secret)

def get_price(symbol, mode='buy'):
    try:
        depth = client.get_order_book(symbol=symbol)
        if depth['asks'] and mode == 'buy':
            price = float(depth['asks'][0][0])
        elif depth['bids'] and mode == 'sell':
            price = float(depth['bids'][0][0])
        else:
            try:
                symbol = reverse_symbol(symbol)
                depth = client.get_order_book(symbol=symbol)
                if depth['asks'] and mode == 'sell':  # Notice the reversal of mode as well
                    price = float(depth['asks'][0][0])
                elif depth['bids'] and mode == 'buy':  # Notice the reversal of mode as well
                    price = float(depth['bids'][0][0])
                else:
                    price = 0.0
            except binance.exceptions.BinanceAPIException:
                price = 0.0
    except:
        try:
            symbol = reverse_symbol(symbol)
            depth = client.get_order_book(symbol=symbol)
            if depth['asks'] and mode == 'sell':  # Notice the reversal of mode as well
                price = float(depth['asks'][0][0])
            elif depth['bids'] and mode == 'buy':  # Notice the reversal of mode as well
                price = float(depth['bids'][0][0])
            else:
                price = 0.0
        except binance.exceptions.BinanceAPIException:
            price = 0.0
    return price



def reverse_symbol(symbol):
    for currency in currencies_all:
        if symbol.endswith(currency):
            currency2 = symbol[:-len(currency)]
            if currency2 in currencies_all:
                return currency + currency2
        if symbol.startswith(currency):
            currency2 = symbol[len(currency):]
            if currency2 in currencies_all:
                return currency2 + currency
def get_pairs_for_currency(currency, tickers):
    pairs = []
    for ticker in tickers:
        if ticker['symbol'].startswith(currency) and len(ticker['symbol'].split(currency)[0]) == 0:
            pairs.append(ticker)
    return pairs

def reform_cycle(cycle):
    try:
        pair_1, pair_2, pair_3  = cycle
        for end in currencies_all:
            if pair_1['symbol'].endswith(end):
                pair_1_end = end
        if not pair_2['symbol'].startswith(pair_1_end):
            pair_2['symbol'] = reverse_symbol(pair_2['symbol'])
        for end in currencies_all:
            if pair_2['symbol'].endswith(end):
                pair_2_end = end
        if not pair_3['symbol'].startswith(pair_2_end):
            pair_3['symbol'] = reverse_symbol(pair_3['symbol'])
    except:
        return

    return pair_1 ,  pair_2 , pair_3

def get_trade_fee(symbol):
    trade_fee = client.get_trade_fee(symbol=symbol)
    try:
        assert(float(trade_fee[0]["takerCommission"]))
        return float(trade_fee[0]["takerCommission"])
    except:
        trade_fee = client.get_trade_fee(symbol=reverse_symbol(symbol))
        return 0.01
def check_arbitrage(cycle):
    try:
        pair_1, pair_2, pair_3 = cycle
        buy_price_1 = float(pair_1["askPrice"])
        if buy_price_1 > 0:
            sell_price_2  = float(pair_2["bidPrice"])
            if sell_price_2 > 0 :
                sell_price_3 = float(pair_3["bidPrice"])
                if sell_price_3 > 0: 
                    initial_investment = 1000
                    after_first_trade = initial_investment / buy_price_1

                    # Получение комиссии для первой пары
                    commission_rate_1 = get_trade_fee(pair_1['symbol'])
                    commission_1 = after_first_trade * commission_rate_1

                    after_first_trade -= commission_1
                    after_second_trade = after_first_trade / sell_price_2

                    # Получение комиссии для второй пары
                    commission_rate_2 = get_trade_fee(pair_2['symbol'])
                    commission_2 = after_second_trade * commission_rate_2

                    after_second_trade -= commission_2
                    final_amount = after_second_trade * sell_price_3

                    # Получение комиссии для третьей пары
                    commission_rate_3 = get_trade_fee(pair_3['symbol'])
                    commission_3 = final_amount * commission_rate_3

                    final_amount -= commission_3
                    profit = final_amount - initial_investment

                    # if profit > 0:
                    print(f"Arbitrage Opportunity: Buy {pair_1['symbol']}, sell {pair_2['symbol']}, sell {pair_3['symbol']}")
                    print(f"Profit: {profit} USD\n")
    except:
        pass
def get_pairs_for_currency_reverse(currency, tickers):
    return [ticker for ticker in tickers if currency in ticker['symbol']]

def reform_cycle_start(cycle):
    try:
        pair_1, pair_2, pair_3  = cycle
        for st in currencies_all:
            if pair_1['symbol'].endswith(st):
                last_sv_1 =  st
                start_sv = pair_1['symbol'].split(st)[0]
                break
        if not pair_2['symbol'].startswith(last_sv_1):
            last_sv_2 = pair_2['symbol'].split(last_sv_1)[0]
            pair_2['symbol'] = last_sv_1 + pair_2['symbol'].split(last_sv_1)[0]
            pair_2["askPrice"] = str(float(pair_2["askPrice"])**-1)
            pair_2["bidPrice"] = str(float(pair_2["bidPrice"])**-1)          

        if not pair_3['symbol'].endswith(start_sv):
            pair_3['symbol'] = pair_3['symbol'].split(start_sv)[1] + start_sv
            pair_3["askPrice"] = str(float(pair_2["askPrice"])**-1)
            pair_3["bidPrice"] = str(float(pair_2["bidPrice"])**-1) 
    except Exception as E:
        print(E)
        return

    return pair_1 ,  pair_2 , pair_3

def analyze_arbitrage_opportunities(tickers):
    for start_currency in currencies_all:
        first_pairs = get_pairs_for_currency_reverse(start_currency, tickers)
        for pair in first_pairs:
            if pair['symbol'].startswith(start_currency) and float(pair['bidPrice']) > 0:  # if start_currency is base currency
                intermediate_currency = pair['symbol'].replace(start_currency, '')
            else:
                continue
            if intermediate_currency:
                second_pairs = get_pairs_for_currency_reverse(intermediate_currency, tickers)
                for second_pair in second_pairs:
                    if second_pair['symbol'].startswith(intermediate_currency) and float(pair['bidPrice']) > 0 :  # if intermediate_currency is base currency
                        end_currency = second_pair['symbol'].replace(intermediate_currency, '')
                    else:  # if intermediate_currency is quote currency
                        if float(second_pair['bidPrice']) > 0:
                            end_currency = second_pair['symbol'].replace(intermediate_currency, '')
                        else:
                            continue
                    if pair['symbol'].startswith(start_currency) and float(pair['bidPrice']) > 0:  # if start_currency is base in first pair
                        end_pair = next((ticker for ticker in tickers if ticker['symbol'] == start_currency + end_currency), None)
                    else:  # if start_currency is quote in first pair
                        if float(end_pair['bidPrice']) > 0:
                            end_pair = next((ticker for ticker in tickers if ticker['symbol'] == end_currency + start_currency), None)
                        else:
                            continue
                    if end_pair:
                        cycle = reform_cycle_start([pair, second_pair, end_pair])
                        check_arbitrage(cycle)

#PROSUSDT USDTBTC BTCPROS
tickers = client.get_ticker()
analyze_arbitrage_opportunities(tickers)