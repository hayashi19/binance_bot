import websocket, pprint

binance_socket  = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
huobi_socket    = "wss://api.huobi.pro"
gaetio_socket   = "wss://fx-ws.gateio.ws/v4/ws/delivery/usdt"
binance_dex_    = "wss://dex.binance.org/api/ws/bnb1m4m9etgf3ca5wpgkqe5nr6r33a4ynxfln3yz4v"

def on_open(ws):
    print('Opened Connection')

def on_close(ws):
    print('Closed Connection')

def on_message(ws, message):
    print(message)

ws = websocket.WebSocketApp(binance_socket, on_open= on_open, on_close= on_close, on_message= on_message)
ws.run_forever()