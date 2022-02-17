import bot_config

data = bot_config.get_data_table('BTCUSDT', '1m', '30')
data.Open.plot()