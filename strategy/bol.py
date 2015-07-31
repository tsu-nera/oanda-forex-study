from strategy.strategy import Strategy


class BOL(Strategy):
    def __init__(self, status):
        Strategy.__init__(self, status)

        self.bolingerband = 0
        self.bol_std = 0
        self.bol_mean = 0
        self.bol_mean_period = 25

    def calc_bol(self, timeseries, event):
        self.bol_mean = \
        timeseries.get_latest_ts_as_df(self.bol_mean_period).mean()[0]
        self.bol_std = \
        timeseries.get_latest_ts_as_df(self.bol_mean_period).std()[0]

        self.bolingerband = 2 * self.bol_std
        self.bol_price_diff = event.bid - self.bol_mean

    def bol_buy_condition(self):
        return self.bol_price_diff > self.bolingerband and self.bol_price_diff > 0

    def bol_sell_condition(self):
        return self.bol_price_diff < self.bolingerband and self.bol_price_diff < 0
