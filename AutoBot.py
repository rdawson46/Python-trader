import alpaca_trade_api as tradeapi


class StockBot(object):
    def __init__(self):
        self.key = 'PK35MDGAXOIF0NSIZ8CC'
        self.secret = ''
        self.url = 'https://paper-api.alpaca.markets'
        self.api = tradeapi.REST(self.key, self.secret, self.url)
        self.symbols = ['CROX', 'VOO']
        self.current_order = None
        self.last_price = 1
        self.positions = []
        self.risk = 0

        for symbol in self.symbols:
            try:
                self.positions.append(int(self.api.get_position(symbol).qty))
            except:
                self.positions.append(0)

    def get_weekly_average(self):
        averages = {}
        barset = self.api.get_barset(self.symbols, 'day', limit=5)

        for symbol in self.symbols:
            stock_barset = barset[symbol]
            total = 0

            for day in stock_barset:
                total += (day.h + day.l) / 2

            averages[symbol] = total / 5

        return averages

    def get_two_week_average(self):
        averages = {}
        barset = self.api.get_barset(self.symbols, 'day', limit=10)

        for symbol in self.symbols:
            stock_barset = barset[symbol]
            total = 0

            for day in stock_barset:
                total += (day.h + day.l) / 2

            averages[symbol] = total / 10

        return averages

    def get_monthly_average(self):
        averages = {}
        barset = self.api.get_barset(self.symbols, 'day', limit=21)

        for symbol in self.symbols:
            stock_barset = barset[symbol]
            total = 0

            for day in stock_barset:
                total += (day.h + day.l) / 2

            averages[symbol] = total / 21

        return averages

    def get_yearly_average(self):
        averages = {}
        barset = self.api.get_barset(self.symbols, 'day', limit=252)

        for symbol in self.symbols:
            stock_barset = barset[symbol]
            total = 0

            for day in stock_barset:
                total += (day.h + day.l) / 2

            averages[symbol] = total / 252

        return averages

    def buy(self, symbol):
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        # figure out how to define buy_quantity and figure out what to so about last price
        buy_quantity = 3
        self.current_order = self.api.submit_order(symbol, buy_quantity, 'buy', 'limit', 'day', self.last_price)
        print(f'Purchasing {buy_quantity} shares of {symbol}')

    def sell(self, symbol):
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        # figure out how to define sell_quantity and figure out what to so about last price
        sell_quantity = 0
        self.current_order = self.api.submit_order(symbol, sell_quantity, 'sell', 'limit', 'day', self.last_price)
        print(f'Selling {sell_quantity} shares of {symbol}')

    @property
    def get_available_balance(self):
        return self.api.get_account().buying_power

    @property
    def get_total(self):
        return self.api.get_account()

    @property
    def is_open(self):
        return self.api.get_clock().is_open

    def algorithm(self):
        # figure out what to do here
        # strategy 1- figure out how to rid the averages and make decisions based of that

        # need to find a way to calculate how much will be bought or sold
        for symbol in self.symbols:
            ...

        pass


if __name__ == '__main__':
    bot = StockBot()
    print(bot.api.get_barset(bot.symbols[0], 'day', limit=1))