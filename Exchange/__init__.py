import ccxt


class ExchangeManager:
    def __init__(self, name, options):
        exchange_class = getattr(ccxt, name)
        self.exchange = exchange_class(options)

    def get_markets(self):
        return self.exchange.load_markets()

    def is_market_exists(self, name):
        return name in self.get_markets()

    def get_ohlcv(self, symbol, since, timeframe='1m'):
        if self.is_market_exists(symbol):
            return self.exchange.fetchOHLCV(symbol, timeframe=timeframe, since=since, limit=1000)
        else:
            return False
