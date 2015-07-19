import numpy as np
from strategy.strategy import Strategy


class Momentum(Strategy):
    def __init__(self, events, status, execution, portfolio):
        Strategy.__init__(self, events, status, execution, portfolio)

        self.period_back = 30
        self.momentum = 0
        self.beta = 0

    def check(self, event):
        self.resample(event)

        momentum_seq = np.asarray(
            self.resampled_prices.tail(self.period_back))

        if len(momentum_seq) < self.period_back:
            return False

        self.beta = (momentum_seq[self.period_back-1] / momentum_seq[0]) * 100

        return self.perform_trade_logic(event,
                                        self.buy_condition,
                                        self.sell_condition)

    def buy_condition(self):
        return self.beta > 100

    def sell_condition(self):
        return self.beta < 100
