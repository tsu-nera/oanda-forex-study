import math
from strategy.strategy import Strategy

# import numpy as np
# import talib


class BolingerBand(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.beta = 0
        self.period = 30

    def calc_indicator(self, timeseries, event):
        # 直接計算
        mean = timeseries.get_latest_ts_as_df(self.period).mean()[0]
        std  = timeseries.get_latest_ts_as_df(self.period).std()[0]

        self.bolingerband = 2 * std
        self.price = event.bid - mean

    def buy_condition(self):
        return self.price > self.bolingerband and self.price > 0

    def sell_condition(self):
        return self.price < self.bolingerband and self.price < 0
