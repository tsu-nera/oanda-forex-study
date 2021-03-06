from strategy.strategy import Strategy
import pandas as pd

# import numpy as np
# import talib


class SMA2(Strategy):
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
        # 直接計算
        mean_short = timeseries.get_latest_ts_as_df(
            self.mean_period_short).mean()[0]
        mean_long = timeseries.get_latest_ts_as_df(
            self.mean_period_long).mean()[0]

        self.sma_short_ts.loc[event.time, event.instrument] = mean_short
        self.sma_long_ts.loc[event.time, event.instrument] = mean_long

        self.beta = mean_short / mean_long

        # talibをつかった場合
        # mean_short_seq = resampled_prices.tail(
        #     self.mean_period_short)[event.instrument]
        # mean_long_seq = resampled_prices.tail(
        #     self.mean_period_long)[event.instrument]
        # mean_short = talib.SMA(np.asarray(mean_short_seq),
        #                        timeperiod=self.mean_period_short)[
        #                            len(mean_short_seq)-1]
        # mean_long = talib.SMA(np.asarray(mean_long_seq),
        #                       timeperiod=self.mean_period_long)[
        #                           len(mean_long_seq)-1]

    def buy_condition(self):
        return self.beta > self.buy_threshold

    def sell_condition(self):
        return self.beta < self.sell_threshold

    def close_buy_condition(self):
        return self.beta < self.sell_threshold

    def close_sell_condition(self):
        return self.beta > self.buy_threshold
