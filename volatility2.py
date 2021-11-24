import time
import schedule
import pyupbit
#import pandas as pd
#from fbprophet import Prophet

#pd.options.display.float_format = "{:.1f}".format
f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()
upbit = pyupbit.Upbit(access, secret)

tick ="KRW-ETH"
def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def buy_crypto_currency(upbit, ticker):
    krw = upbit.get_balance(ticker)[2]
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook[0]['orderbook_units'][0]['ask_price']
    unit = krw/float(sell_price) * 0.7
    return upbit.buy_market_order(ticker, unit)

def sell_crypto_currency(upbit, ticker):
    unit = upbit.get_balance(ticker)
    return upbit.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]

def get_ma15(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_ma20(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def get_ma30(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma30 = df['close'].rolling(30).mean().iloc[-1]
    return ma30

def get_ma60(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=60)
    ma60 = df['close'].rolling(60).mean().iloc[-1]
    return ma60

def change_ticker(string):
    global tick
    tick = "KRW-"+string
    print(tick)
    return tick

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

predicted_close_price = 0
# def predict_price(ticker):
#     """Prophet으로 당일 종가 가격 예측"""
#     global predicted_close_price
#     df = pyupbit.get_ohlcv(ticker, interval="minute60")
#     df = df.reset_index()
#     df['ds'] = df['index']
#     df['y'] = df['close']
#     data = df[['ds','y']]
#     model = Prophet()
#     model.fit(data)
#     future = model.make_future_dataframe(periods=24, freq='H')
#     forecast = model.predict(future)
#     closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
#     if len(closeDf) == 0:
#         closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
#     closeValue = closeDf['yhat'].values[0]
#     predicted_close_price = closeValue
# predict_price("KRW-BTC")
# schedule.every().hour.do(lambda: predict_price("KRW-BTC"))
#
