import numpy as np
import pandas as pd


class TimeSeries():
    def __init__(self, is_sim):

        self.resample_interval = '5s'
        self.is_sim = is_sim

        self.prices = pd.DataFrame()
        self.buys = pd.DataFrame()
        self.sells = pd.DataFrame()

        self.resampled_prices = None

    def add_tick_event(self, event):
        self.prices.loc[event.time, event.instrument] = event.bid

        self.resampled_prices = self.prices.resample(
            self.resample_interval,
            how='last',
            fill_method="ffill")

        if not self.is_sim and len(self.resampled_prices) > 1000:
            self.resampled_prices.drop(self.resampled_prices(1).index)

    def add_buy_event(self, event):
        self.buys.loc[event.time, event.instrument] = event.bid

    def add_sell_event(self, event):
        self.sells.loc[event.time, event.instrument] = event.ask

    def get_latest_ts_as_df(self, period):
        return self.resampled_prices.tail(period)

    def get_latest_ts_as_array(self, period, event):
        return np.asarray(self.get_latest_ts_as_df(period)[event.instrument])
