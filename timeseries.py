import numpy as np
import pandas as pd


class TimeSeries():
    def __init__(self):

        self.resample_interval = '60s'

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

    def add_buy_event(self, event):
        self.buys.loc[event.time, event.instrument] = event.bid

    def add_sell_event(self, event):
        self.sells.loc[event.time, event.instrument] = event.ask

    def get_latest_ts_as_df(self, period):
        return self.resampled_prices.tail(period)

    def get_latest_ts_as_array(self, period, event):
        return np.asarray(self.get_latest_ts_as_df(period)[event.instrument])

    # def get_latest_event(self):
    #     # TODO 確認
    #     return self.resampled_prices.tail(1)[0]
