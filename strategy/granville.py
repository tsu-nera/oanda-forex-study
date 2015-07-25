from strategy.strategy import Strategy
import pandas as pd
import statsmodels.api as sm

import numpy as np
# import talib


class Granville(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.beta_pre = 0
        self.beta = 0
        self.mean_period_short = 20
        self.mean_period_long = 40
        self.buy_threshold = 1.0
        self.sell_threshold = 1.0

        self.sma_short_ts = pd.DataFrame()
        self.sma_long_ts = pd.DataFrame()
        self.sma_ols_ts = pd.DataFrame()

        self.mean_for_ols_period = 6
        self.ols_period = 40

        self.a = 0
        self.b = 0

    def calc_indicator(self, timeseries, event):
        mean_short = timeseries.get_latest_ts_as_df(
            self.mean_period_short).mean()[0]
        mean_long = timeseries.get_latest_ts_as_df(
            self.mean_period_long).mean()[0]
        mean_for_ols = timeseries.get_latest_ts_as_df(
            self.mean_for_ols_period ).mean()[0]

        if timeseries.is_sim:
            self.sma_short_ts.loc[event.time, event.instrument] = mean_short
            self.sma_long_ts.loc[event.time, event.instrument] = mean_long

        self.sma_ols_ts.loc[event.time, event.instrument] = mean_for_ols

        self.beta_pre = self.beta
        self.beta = mean_short / mean_long

        x = range(self.ols_period)
        y = np.asarray(
            self.sma_ols_ts.tail(self.ols_period)[event.instrument])

        if len(y) < len(x):
            return

        results = sm.OLS(y, sm.add_constant(x), prepend=True).fit()
        self.a, self.b = results.params

        self.cleanup_data()

    def buy_condition(self):
        return self.beta > 1.0 and self.beta_pre < 1.0 and self.b > 0

    def close_buy_condition(self):
        return self.beta < 1.0 and self.beta_pre > 1.0 and self.b < 0

    def sell_condition(self):
        return self.beta < 1.0 and self.beta_pre > 1.0 and self.b < 0

    def close_sell_condition(self):
        return self.beta > 1.0 and self.beta_pre < 1.0 and self.b > 0

    def print_beta(self):
        print("%s/%s" % (self.beta_pre, self.beta))

    def cleanup_data(self):
        if len(self.sma_ols_ts) > self.ols_period:
            self.sma_ols_ts.drop(self.sma_ols_ts.head(1).index)
