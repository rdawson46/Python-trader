import alpaca_trade_api as alpaca


class Trader(object):
    def __init__(self):
        self.key = 'PK35MDGAXOIF0NSIZ8CC'
        self.secret = ''
        self.url = 'https://paper-api.alpaca.markets'
        self.api = alpaca.REST(self.key, self.secret, self.url)
        self.symbols = ['CROX', 'VOO']
        self.current_order = None
        self.last_price = 1
        self.positions = []

        for symbol in self.symbols:
            try:
                self.positions.append(int(self.api.get_position(symbol).qty))
            except:
                self.positions.append(0)

    def interaction_menu(self):
        print("-------Trading Interface-------")
        for i in range(len(self.symbols)):
            print(f'{i+1}. {self.symbols[i]}')

        print(f'{len(self.symbols) + 1}. Check balance')
        print(f'{len(self.symbols) + 2}. Check Positions')

        choice = int(input("Select an Option: "))

        if choice > len(self.symbols) + 2:
            choice = int(input("Select a valid option:  "))

        if choice == len(self.symbols) + 1:
            # calls method to check the total balance
            print(int(self.api.get_account().portfolio_value) - int(self.api.get_account().cash))

        elif choice == len(self.symbols) + 2:
            # calls method to check positions for every stock
            for symbol in self.symbols:
                try:
                    print(f'{symbol}) {self.api.get_position(symbol)} shares')
                except:
                    print(f'{symbol}) No position found')

        else:
            stock = self.symbols[choice - 1]
            print(f"\nOptions for {stock}")
            print("1. Buy\n2. Sell")

            choice = 0
            while not 1 <= choice <= 2:
                choice = int(input("Enter Option Number: "))

            if choice == 1:
                # calls method to buy chosen stock
                self.buy(stock)

            elif choice == 2:
                # calls method to sell chosen stock
                self.sell(stock)

    def buy(self, symbol):
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        buy_quantity = 0

        # add check to make sure the user can afford to buy that number of shares
        while buy_quantity == 0:
            buy_quantity = int(input("How many shares would you like to buy: "))

        self.current_order = self.api.submit_order(symbol, buy_quantity, 'buy', 'market', 'day')
        print(f'Buying {buy_quantity} shares of {symbol}')

    def sell(self, symbol):
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        sell_quantity = 0

        # add a check to make sure that the user has that many shares
        while sell_quantity == 0:
            sell_quantity = int(input("How many shares would you like to sell: "))

        self.current_order = self.api.submit_order(symbol, sell_quantity, "sell", 'market', 'day')
        print(f'Selling {sell_quantity} shares of {symbol}')


if __name__ == "__main__":
    x = Trader()
    x.interaction_menu()

