from strategy.strategy import Strategy
import pandas as pd


class SMA(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.sma = 0
        self.sma_pre = 0
        self.mean_period_short = 25
        self.mean_period_long = 75
        self.sma_mean_short = 0
        self.sma_mean_long = 0
        self.sma_short_ts = pd.DataFrame()
        self.sma_long_ts = pd.DataFrame()

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)

    def calc_sma(self, timeseries, event):
        self.sma_mean_short_pre = self.sma_mean_short
        self.sma_mean_long_pre = self.sma_mean_long

        self.sma_mean_short = timeseries.get_latest_ts_as_df(
            self.mean_period_short).mean()[0]
        self.sma_mean_long = timeseries.get_latest_ts_as_df(
            self.mean_period_long).mean()[0]

        if self.status["is_sim"]:
            self.sma_short_ts.loc[event.time, event.instrument] \
                = self.sma_mean_short
            self.sma_long_ts.loc[event.time, event.instrument] \
                = self.sma_mean_long

    def sma_buy_condition(self):
        return self.sma_mean_short_pre < self.sma_mean_long_pre \
            and self.sma_mean_short > self.sma_mean_long

    def sma_sell_condition(self):
        return self.sma_mean_short_pre > self.sma_mean_long_pre \
            and self.sma_mean_short < self.sma_mean_long

    def buy_condition(self):
        return self.sma_buy_condition()

    def close_buy_condition(self, event):
        return self.sma_sell_condition()

    def sell_condition(self):
        return self.sma_sell_condition()

    def close_sell_condition(self, event):
        return self.sma_buy_condition()

    def print_data(self):
        print("sma_short=%s sma_long=%s"
              % (self.sma_mean_short, self.sma_mean_long))
