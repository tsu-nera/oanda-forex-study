from strategy.strategy import Strategy
import pandas as pd

import numpy as np
import statsmodels.api as sm
# import talib


class SMARSIOLS(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.rsi = 50
        self.rsi_period = 10

        self.beta = 0
        self.beta_pre = 0
        self.mean_period_short = 20
        self.mean_period_long = 40
        self.buy_threshold = 1.0
        self.sell_threshold = 1.0
        self.sma_short_ts = pd.DataFrame()
        self.sma_long_ts = pd.DataFrame()

        self.sma_ols_ts = pd.DataFrame()
        self.mean_for_ols_period = 20
        self.ols_period = 20
        self.a = 0
        self.b = 0
        self.pre_b = 0

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)
        self.calc_rsi(timeseries, event)
        self.calc_ols(timeseries, event)

    def calc_ols(self, timeseries, event):
        mean_for_ols = timeseries.get_latest_ts_as_df(
            self.mean_for_ols_period).mean()[0]

        self.sma_ols_ts.loc[event.time, event.instrument] = mean_for_ols

        x = range(self.ols_period)
        y = np.asarray(
            self.sma_ols_ts.tail(self.ols_period)[event.instrument])

        if len(y) < len(x):
            return

        results = sm.OLS(y, sm.add_constant(x), prepend=True).fit()
        self.pre_b = self.b
        self.a, self.b = results.params

    def calc_rsi(self, timeseries, event):
        delta = timeseries.get_latest_ts_as_df(
            self.rsi_period).diff()

        if len(delta) < self.rsi_period:
            return

        diff_up, diff_down = delta.copy(), delta.copy()
        diff_up[diff_up < 0] = 0
        diff_down[diff_down > 0] = 0

        rol_up = diff_up.mean()[0]
        rol_down = diff_down.mean().abs()[0]

        rs = rol_up / rol_down
        self.rsi = 100.0 - (100.0 / (1.0 + rs))

    def calc_sma(self, timeseries, event):
        mean_short = timeseries.get_latest_ts_as_df(
            self.mean_period_short).mean()[0]
        mean_long = timeseries.get_latest_ts_as_df(
            self.mean_period_long).mean()[0]

        self.sma_short_ts.loc[event.time, event.instrument] = mean_short
        self.sma_long_ts.loc[event.time, event.instrument] = mean_long

        self.beta_pre = self.beta
        self.beta = mean_short / mean_long

    def is_range(self):
        return self.rsi > 40 and self.rsi < 60

    def buy_condition(self):
        return (self.beta > 1.0 and self.beta_pre < 1.0 \
                or self.pre_b < 0 and self.b > 0) \
                and not self.is_range()

    def close_buy_condition(self):
        return self.pre_b >= 0 and self.b < 0

    def sell_condition(self):
        return (self.beta < 1.0 and self.beta_pre > 1.0 \
                or self.pre_b >= 0 and self.b < 0) \
                and not self.is_range()

    def close_sell_condition(self):
        return self.pre_b <= 0 and self.b > 0
