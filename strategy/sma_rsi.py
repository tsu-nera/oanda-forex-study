from strategy.sma import SMA
from strategy.rsi import RSI


class SMARSI(SMA, RSI):
    def __init__(self, status):
        SMA.__init__(self, status)
        RSI.__init__(self, status)

        self.rsi_period = 75

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)
        self.calc_rsi(timeseries, event)

    def buy_condition(self):
        return self.sma_buy_condition() and self.is_up()

    def close_buy_condition(self, event):
        return self.sma_sell_condition()

    def sell_condition(self):
        return self.sma_sell_condition() and not self.is_up()

    def close_sell_condition(self, event):
        return self.sma_buy_condition()
