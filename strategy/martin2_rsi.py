from strategy.rsi import RSI
from strategy.time import Time
from strategy.martingale2 import MARTIN2

class MARTIN2RSI(MARTIN2, RSI, Time):
    def __init__(self, status):
        MARTIN2.__init__(self, status)
        RSI.__init__(self, status)
        Time.__init__(self, status)

    def calc_indicator(self, timeseries, event):
        self.calc_rsi(timeseries, event)
        self.calc_martin(timeseries, event)

    def buy_condition(self, event):
        return self.rsi_buy_condition() \
            and not self.time_close_guard_condition(event)

    def close_buy_condition(self, event):
        return self.martin_close_condition(event) 

    def sell_condition(self, event):
        return self.rsi_sell_condition() \
            and not self.time_close_guard_condition(event)

    def close_sell_condition(self, event):
        return self.martin_close_condition(event) 
