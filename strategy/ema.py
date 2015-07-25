from strategy.strategy import Strategy
import pandas as pd

import talib


class EMA(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.beta = 0
        self.mean_period_short = 20
        self.mean_period_long = 40
        self.buy_threshold = 1.0
        self.sell_threshold = 1.0

        self.sma_short_ts = pd.DataFrame()
        self.sma_long_ts = pd.DataFrame()

    def calc_indicator(self, timeseries, event):
        mean_short_seq = timeseries.get_latest_ts_as_array(
            self.mean_period_short, event)
        mean_long_seq = timeseries.get_latest_ts_as_array(
            self.mean_period_long, event)
        mean_short = talib.EMA(mean_short_seq,
                               timeperiod=self.mean_period_short)[
                                   len(mean_short_seq)-1]
        mean_long = talib.EMA(mean_long_seq,
                              timeperiod=self.mean_period_long)[
                                  len(mean_long_seq)-1]

        self.sma_short_ts.loc[event.time, event.instrument] = mean_short
        self.sma_long_ts.loc[event.time, event.instrument] = mean_long

        self.beta = mean_short / mean_long

    def buy_condition(self):
        return self.beta > self.buy_threshold

    def sell_condition(self):
        return self.beta < self.sell_threshold