# Import libary to configurate to bot to binance api server and add some simple strategy command
import api_config, websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import * 

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'BTCUSDT'
TRADE_QUANTITY = 0.00024
position = False
closes = []

client = Client(api_config.api_key, api_config.api_secret)

def order(symbol, quantity, side, order_type=ORDER_TYPE_MARKET):
    try:
        order = client.create_test_order(symbol=symbol, side=side, quantity=quantity, type=order_type, )
        print(order)
    except Exception as e:
        return False
    return True


def on_open(ws):
    print('Opened Connection')

def on_close(ws):
    print('Closed Connection')

def on_message(ws, message):
    global closes
    global position
    json_message    = json.loads(message)
    # pprint.pprint(json_message)
    candle          = json_message['k']
    is_canlde_close = candle['x']
    candle_close    = candle['c']
    canlde_symbol   = candle['s']

    if is_canlde_close:
        # print(canlde_symbol + " closed at " + candle_close)
        closes.append(float(candle_close))
        # print(closes)

        if len(closes) > RSI_PERIOD:
            np_close = numpy.array(closes)
            rsi = talib.RSI(np_close, RSI_PERIOD)

            last_rsi = rsi[-1]
            print(last_rsi)

            if last_rsi > RSI_OVERBOUGHT:
                if position:
                    print("SELL")
                    # ORDER SELL BINANCE
                    order_succeeded = order(TRADE_SYMBOL, SIDE_SELL, TRADE_QUANTITY)
                    print(order_succeeded)
                    if order_succeeded:
                        position = False
                else:
                    print("No oerder posistion yet")

            if last_rsi < RSI_OVERSOLD:
                if position:
                    print("Already in posistion")
                else:
                    print("BUY")
                    # ORDER BUY BINANCE
                    order_succeeded = order(TRADE_SYMBOL, SIDE_BUY, TRADE_QUANTITY)
                    print(order_succeeded)
                    if order_succeeded:
                        position = True

ws = websocket.WebSocketApp(SOCKET, on_open= on_open, on_close= on_close, on_message= on_message)
ws.run_forever()