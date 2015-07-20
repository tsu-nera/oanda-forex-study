import numpy as np
from strategy.strategy import Strategy


class Momentum(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.period_back = 30
        self.momentum = 0
        self.beta = 0

    def calc_indicator(self, timeseries, event):
        momentum_seq = timeseries.get_latest_ts_as_array(
            self.period_back, event)

        if len(momentum_seq) < self.period_back:
            return False

        self.beta = (momentum_seq[self.period_back-1] / momentum_seq[0]) * 100

    def buy_condition(self):
        return self.beta > 100

    def sell_condition(self):
        return self.beta < 100
