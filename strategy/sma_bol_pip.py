from strategy.strategy import Strategy
import pandas as pd

class SMABOLPIP(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.beta = 0
        self.beta_pre = 0
        self.mean_period_short = 20
        self.mean_period_long = 40
        self.buy_threshold = 1.0
        self.sell_threshold = 1.0

        self.sma_short_ts = pd.DataFrame()
        self.sma_long_ts = pd.DataFrame()

        self.price = 0
        self.bolingerband = 0

    def calc_indicator(self, timeseries, event):
        mean_short = timeseries.get_latest_ts_as_df(
            self.mean_period_short).mean()[0]
        mean_long = timeseries.get_latest_ts_as_df(
            self.mean_period_long).mean()[0]

        if self.status["is_sim"]:
            self.sma_short_ts.loc[event.time, event.instrument] = mean_short
            self.sma_long_ts.loc[event.time, event.instrument] = mean_long

        self.beta_pre = self.beta
        self.beta = mean_short / mean_long

        std = timeseries.get_latest_ts_as_df(self.mean_period_short).std()[0]

        self.bolingerband = 2 * std
        self.price = event.bid - mean_short

    def buy_condition(self):
        return self.beta > 1.0 and self.beta_pre < 1.0 \
            or (abs(self.price) > self.bolingerband and self.price < 0)

    def close_buy_condition(self, event):
        return abs(self.status["opening_price"] - event.bid) > 0.0005

    def sell_condition(self):
        return self.beta < 1.0 and self.beta_pre > 1.0 \
            or (abs(self.price) > self.bolingerband and self.price > 0)

    def close_sell_condition(self, event):
        return abs(self.status["opening_price"] - event.bid) > 0.0005
