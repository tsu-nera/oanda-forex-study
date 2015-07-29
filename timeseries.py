import numpy as np
import pandas as pd


class TimeSeries():
    def __init__(self, status):

        self.resample_interval = '5s'

        self.prices = pd.DataFrame()
        self.buys = pd.DataFrame()
        self.sells = pd.DataFrame()
        self.close_wins = pd.DataFrame()
        self.close_loses = pd.DataFrame()
        self.status = status

        self.resampled_prices = None

    def add_tick_event(self, event):
        self.prices.loc[event.time, event.instrument] = event.bid

        self.resampled_prices = self.prices.resample(
            self.resample_interval,
            how='last',
            fill_method="ffill")

        if len(self.resampled_prices) > 1000:
            self.resampled_prices.drop(self.resampled_prices.index[[0]])
        if len(self.prices) > 1000:
            self.prices.drop(self.prices.index[[0]])

    def add_buy_event(self, event):
        self.buys.loc[event.time, event.instrument] = event.bid

    def add_sell_event(self, event):
        self.sells.loc[event.time, event.instrument] = event.bid

    def add_close_win_event(self, event):
        self.close_wins.loc[event.time, event.instrument] = event.bid

    def add_close_lose_event(self, event):
        self.close_loses.loc[event.time, event.instrument] = event.bid

    def get_latest_ts_as_df(self, period):
        return self.resampled_prices.tail(period)

    def get_latest_ts_as_array(self, period, event):
        return np.asarray(self.get_latest_ts_as_df(period)[event.instrument])
