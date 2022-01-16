import pandas as pd
import math
import random
random.seed(100) # for debugging

EPSILON = 0.0005

class AbstractBot:
    def action(self, daily_data, balance, stocks):
        raise Exception("Can't call abstract method")

class SimpleBot(AbstractBot):
    def __init__(self):
        pass

    def action(self, daily_data, balance, stocks):
        '''
        Given data until today, long / short some number of stocks
        Returns number of securities to long (negative means short)
        '''
        price = daily_data[-1]
        if balance > EPSILON:
            if random.random() > 0.5:
                return balance / price
        else:
            if random.random() > 0.5:
                return -stocks
        return 0

class Simulator:
    def __init__(self, daily_data, bot, init_balance, allow_short_pos=False):
        self.daily_data = daily_data
        throw_if_nan(self.daily_data)
        self.bot = bot
        self.balance = init_balance
        self.stocks = 0
        self.allow_short_pos = allow_short_pos

        assert isinstance(bot, AbstractBot)

    def simulate(self, init_cut):
        '''
        init_cut is the first today
        '''
        # k is today
        for k in range(init_cut, len(self.daily_data) - 2):
            action = self.bot.action(self.daily_data[:k+1], self.balance, self.stocks)
            self.process(action, k)
            if not self.allow_short_pos and (self.balance < -EPSILON or self.stocks < -EPSILON * self.daily_data[k]):
                raise Exception('Cash or Securities position is negative when short position is not allowed.')
        return (self.balance, self.stocks * self.daily_data[-1])

    def process(self, stocks, today):
        '''
        Process `stocks` securities
        Negative means short
        '''
        self.stocks += stocks
        self.balance -= stocks * self.daily_data[today]

def throw_if_nan(arr):
    if any(map(lambda val: math.isnan(val), arr)):
        raise ValueError('Arr contains nan!')

if __name__ == "__main__":
    raw_data = pd.read_csv('./DOGE-USD.csv', sep=',')
    data = raw_data[["Close"]].to_numpy().T[0]
    clean_data = list(filter(lambda val: not math.isnan(val), data))
    bot = SimpleBot()
    sim = Simulator(clean_data, bot, 100)
    end_pos = sim.simulate(0)
    print(end_pos)
