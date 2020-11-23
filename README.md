# CryptoDL

CryptoDL aims to provide only historical OHLCV data from different cryptocurrency exchange platform.
It uses CCXT package (https://github.com/ccxt/ccxt) to connect directly to many different exchange.

## Dependencies
CryptoDL use some external dependencies that you have to install :
```shell script
pip install ccxt
pip install shlex
```

## Commands list :

#####List All Exchange Platform :
```
[Cryptodl] list_platform
```

##### List All Market's from an Exchange Platform
```
[Cryptodl] list_markets <platform_name>
```

##### Download Historical Data
```
[Cryptodl] download -p <platform-name> -s <symbol> -db <db-file> [-t <table-name> -f <timeframe>]
```

##### Get Candles Cursor
Get range of candle between date and offset in the specified db-file
```
[Cryptodl] get_candles_cursor -db <db-file> -d <date> [-t <table> -l <limit_offset>]
```

##### Get last Candle
Get the last Candle in the specified db-file
```
[Cryptodl] get_last_candle -db <db-file> [-t <table>]
```

##### Get first Candle
```
[Cryptodl] get_last_candle -db <db-file> [-t <table>]
```

##### Get Candles
Get All candles from the specified db-file (be carefull some db-file can be large)
```
[Cryptodl] get_candles -db <db-file> [-t <table>]
```