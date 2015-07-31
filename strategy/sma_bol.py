from strategy.sma import SMA
from strategy.bol import BOL

class SMABOL(SMA, BOL):
    def __init__(self, status):
        SMA.__init__(self, status)
        BOL.__init__(self, status)

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)
        self.calc_bol(timeseries, event)

    def buy_condition(self):
        return self.sma_buy_condition() \
            or self.bol_buy_condition()

    def close_buy_condition(self, event):
        return self.sma_sell_condition()

    def sell_condition(self):
        return self.sma_sell_condition() \
            or self.bol_sell_condition()

    def close_sell_condition(self, event):
        return self.sma_buy_condition()        
