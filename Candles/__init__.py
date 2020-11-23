
from Database import Connector
from Exchange import ExchangeManager
from datetime import datetime
from datetime import timedelta


class DBCandleManager:
    def __init__(self, path, table):
        self.db = Connector(path)
        self.table = table
        self.db.connect()

    def create_table(self):
        self.db.create_table(f'''CREATE TABLE IF NOT EXISTS {self.table}(
            id INTEGER PRIMARY KEY,
            date INTEGER NOT NULL UNIQUE,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL);''')

    def insert(self, candle):
        self.db.insert(f'INSERT INTO {self.table} (date,open,high,low,close,volume) VALUES({candle[0]},{candle[1]},{candle[2]},{candle[3]},{candle[4]},{candle[5]});')

    def get_last_candle(self):
        self.create_table()
        result = self.db.select(f'SELECT * FROM {self.table} ORDER BY date DESC LIMIT 1')
        if len(result) > 0:
            return result[0]
        else:
            return 'null'

    def get_first_candle(self):
        self.create_table()
        result = self.db.select(f'SELECT * FROM {self.table} ORDER BY date ASC LIMIT 1')
        if len(result) > 0:
            return result[0]
        else:
            return 'null'

    def get_candles_cursor(self, start, offset):
        start = datetime.fromtimestamp(start / 1e3) - timedelta(minutes=offset)
        start = int(datetime.timestamp(start)) * 1e3
        self.create_table()
        results = self.db.select(f'SELECT * FROM {self.table} WHERE date > {start} ORDER BY date LIMIT {offset}')
        return results

    def get_candles(self):
        self.create_table()
        results = self.db.select(f'SELECT * FROM {self.table}')
        return results


class PlatformCandleManager:
    def __init__(self, exchange, symbol):
        self.exchange = ExchangeManager(exchange, {"enableRateLimit": True})
        self.symbol = symbol

    def load_candles(self, since, timeframe="1m"):
        return self.exchange.get_ohlcv(self.symbol, since, timeframe)


class CandleDownloader:
    def __init__(self, exchange, symbol, name, table):
        self.exchange = exchange
        self.name = name
        self.symbol = symbol
        self.table = table

    def download(self, timeframe='1m'):
        dbm = DBCandleManager(f'{self.name}', self.table)
        pm = PlatformCandleManager(self.exchange, self.symbol)
        state = False
        while True:
            last_candle = dbm.get_last_candle()

            if last_candle == 'null':
                last_candle = datetime.timestamp(datetime.fromisoformat('2000-01-01'))
                last_candle = int(last_candle)
            else:
                last_candle = last_candle[1]
                if timeframe == '1m':
                    last_candle = datetime.fromtimestamp(last_candle / 1e3) + timedelta(minutes=1)
                elif timeframe == '5m':
                    last_candle = datetime.fromtimestamp(last_candle / 1e3) + timedelta(minutes=5)
                elif timeframe == '1h':
                    last_candle = datetime.fromtimestamp(last_candle / 1e3) + timedelta(hours=1)
                last_candle = datetime.timestamp(last_candle)
                last_candle = int(last_candle * 1e3)

            candles = pm.load_candles(last_candle, timeframe)
            if len(candles) < 2:
                break
            print(f'Downloading [{datetime.fromtimestamp(candles[0][0] / 1e3)}... to ...{datetime.fromtimestamp(candles[len(candles) - 1][0] / 1e3)}]')
            for candle in candles:
                dbm.insert(candle)
            state = True
        return state

