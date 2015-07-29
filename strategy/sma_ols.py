from strategy.sma import SMA
from strategy.ols import OLS


class SMAOLS(SMA, OLS):
    def __init__(self, status):
        SMA.__init__(self, status)
        OLS.__init__(self, status)

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)
        self.calc_ols(timeseries, event)

    def buy_condition(self):
        return self.sma_buy_condition() \
            or self.ols_buy_condition()

    def close_buy_condition(self, event):
        return self.ols_sell_condition()

    def sell_condition(self):
        return self.sma_sell_condition() \
            or self.ols_sell_condition()

    def close_sell_condition(self, event):
        return self.ols_buy_condition()

    def cleanup_data(self):
        if len(self.sma_ols_ts) > self.ols_period:
            self.sma_ols_ts.drop(self.sma_ols_ts.head(1).index)
