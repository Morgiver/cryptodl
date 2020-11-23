import ccxt
import shlex

from Candles import CandleDownloader
from Candles import DBCandleManager
from cmd import Cmd
from datetime import datetime


class ShellArgumentsParser:
    def __init__(self, args):
        args = shlex.split(args)

        last_arg_name = None

        for arg in args:
            if arg[0] != '-' and last_arg_name is not None:
                self.__dict__[last_arg_name] = arg
            else:
                last_arg_name = arg[1:]

    def default(self, key, value):
        if not hasattr(self, key):
            self.__dict__[key] = value

    def required(self, key):
        if not hasattr(self, key):
            raise AttributeError(f"Parameter -{key} is required")


class BobotShell(Cmd):
    intro = "=========== Welcome on Cryptodl ==========\n\n" \
            " This Application aims to provide only historical \n" \
            " OHLCV data from different cryptocurrency exchange platform.\n" \
            " It uses CCXT package ( https://github.com/ccxt/ccxt ) to \n" \
            " connect directly to many different exchange. \n\n" \
            "Here's an example on how to use Cryptodl : \n" \
            "------------------------------------------\n\n" \
            " First type the command : list_platform \n" \
            " Choose a platform and type the command : \n" \
            "  list_markets <name_of_your_choosen_platform> \n" \
            "  Example : list_markets binance \n" \
            " Choose a Market and finaly type the command like :\n" \
            "  download -p <platform-name> -s <symbol> -db <db-file> \n" \
            "  Example : download -p binance -s BTC/USDT -db btc-usdt-binance-1m.db \n" \
            " After that, make some coffee, it will take some times ;)\n\n" \
            "If you want to know more about all commands :\n" \
            "---------------------------------------------\n\n " \
            "You can type '?' or 'help' to list all commands \n" \
            " You can type '? <command_name>' or 'help <command_name>'\n\n" \
            "If you're satisfied by this tiny app and want to support,\n " \
            "don't hesitate to buy me a coffee with BTC ;)\n" \
            "BTC : 3G85t2xqaogBZJ5Y7XdKirocwf2DNTuZiN \n"
    prompt = '[Cryptodl] '

    def do_get_candle(self, args):
        """Get Candle
    Use :  get_candle -db <db-file> [-t <table>]
    Description : get candle from a platform and symbol
        """
        try:
            args = ShellArgumentsParser(args)
            args.default('t', 'candles')
            args.required('db')

            c = DBCandleManager(args.db, args.t)
            print(c.get_candles())
        except AttributeError as err:
            print(err)

    def do_get_first_candle(self, args):
        """Get First Candle
    Use : get_first_candle -db <db-file> [-t <table>]
    Description : get first candle in the DB
        """
        try:
            args = ShellArgumentsParser(args)
            args.default('t', 'candles')
            args.required('db')

            c = DBCandleManager(args.db, args.t)
            print(c.get_first_candle())
        except AttributeError as err:
            print(err)

    def do_get_last_candle(self, args):
        """Get Last Candle
    Use : get_last_candle -db <db-file> [-t <table>]
    Description : get last candle in the DB
        """
        try:
            args = ShellArgumentsParser(args)
            args.default('t', 'candles')
            args.required('db')

            c = DBCandleManager(args.db, args.t)
            print(c.get_last_candle())
        except AttributeError as err:
            print(err)

    def do_get_candles_cursor(self, args):
        """Get Candle Cursor
    Use : get_candles_cursor -db <db-file> -d <date> [-t <table> -l <limit_offset>]
    Description : get range of candle between date and offset
        """
        try:
            args = ShellArgumentsParser(args)
            args.default('t', 'candles')
            args.default('l', 500)
            args.required('db')
            args.required('d')

            args.d = int(datetime.timestamp(datetime.fromisoformat(args.d))) * 1e3

            c = DBCandleManager(args.db, args.t)
            candles = c.get_candles_cursor(args.d, args.l)

            for candle in candles:
                print(candle)

        except AttributeError as err:
            print(err)

    def do_list_platform(self, args):
        """List Exchange Platform :
    Use : list_platform
    Description : List all platform names you can use"""
        for name in ccxt.exchanges:
            print(name)

    def do_list_markets(self, args):
        """List All Markets Platform's
    Use : list_markets <platform>
    Description : List all market names from a platform"""
        if args in ccxt.exchanges:
            exchange_class = getattr(ccxt, args)
            exchange = exchange_class()
            for name in exchange.load_markets():
                print(name)

    def do_download(self, args):
        """Download a Market :
    Use: download -p <platform-name> -s <symbol> -db <db-file> [-t <table-name> -f <timeframe>]
    Description : With this cmd you can download any market from any supported
                  platform by CCXT library ( https://github.com/ccxt/ccxt ).
        """
        try:
            args = ShellArgumentsParser(args)
            args.default('t', 'candles')
            args.default('f', '1m')
            args.required('p')
            args.required('s')
            args.required('db')

            d = CandleDownloader(args.p, args.s, args.db, args.t)
            result = d.download(args.f)

            if not result:
                print(f"Market {args.s} on {args.p} doesn't exist or something went wrong")
            else:
                print(f'Market {args.s} Downloaded on {args.p} !')
        except AttributeError as err:
            print(err)

    def do_quit(self, args):
        """Quit application"""
        print('Thx for using Cryptodl :) ')
        return True


if __name__ == '__main__':
    BobotShell().cmdloop()
